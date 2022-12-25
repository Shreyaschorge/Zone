import os
from sanic import Blueprint, response
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm.exc import NoResultFound
from zone_common.exceptions import RequestValidationException, NotFoundException, BadRequestException
from zone_common.middlewares.require_auth import require_auth
from zone_common.events.order_status import OrderStatus
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload, subqueryload
from sqlalchemy.sql.expression import column, and_

from models.order_products import OrderProduct
from models.order import Order
from models.product import Product
from schema.order import OrderSchema
from schema.product import ProductSchema

order = Blueprint(name="order", url_prefix="/api/orders")

order_schema = OrderSchema()
list_product_schema = ProductSchema(many=True)


@order.get('/')
@require_auth
async def all_users_orders(req):
    session = req.ctx.session
    userId = req.ctx.current_user["uuid"]
    async with session.begin():
        q = select(Order).where(Order.userId == userId).options(
            selectinload(Order.products))
        result = await session.execute(q)
        all_orders = result.scalars().all()
    return response.json([order.to_dict() for order in all_orders], status=200)


@order.get("/<uuid>")
@require_auth
async def single_order(req, uuid):
    session = req.ctx.session
    async with session.begin():
        q = select(Order).where(Order.uuid == uuid).options(
            selectinload(Order.products))

        try:
            result = await session.execute(q)
            existing_order = result.scalars().one()
        except NoResultFound:
            raise NotFoundException()

    if existing_order.userId != req.ctx.current_user["uuid"]:
        raise BadRequestException("Can't access orders of another user")

    return response.json(existing_order.to_dict(), status=200)


@order.post('/')
@require_auth
async def create_order(req):

    session = req.ctx.session
    current_user = req.ctx.current_user
    payload = req.json

    def getProductQuantity(product):
        quantity = None
        for _prod in payload:
            if (_prod["productId"] == product.uuid):
                quantity = _prod["quantity"]
                break
        return quantity

    async with session.begin():

        productIds = list(map(lambda x: x["productId"], payload))

        q = select(Product).filter(Product.uuid.in_(productIds))

        result = await session.execute(q)
        existing_products = result.scalars().all()

        if len(existing_products) != len(payload):
            raise NotFoundException()

        order = Order(products=existing_products)
        order.userId = current_user["uuid"]
        session.add(order)

        order_products = []

        for product in existing_products:
            order_products.append(OrderProduct(
                order=order, product=product, quantity=getProductQuantity(product)))

        for order_product in order_products:
            session.add(order_product)

        await session.commit()

    return response.json({"message": "Order is been created"}, status=201)


@order.put("/cancelOrder/<uuid>")
@require_auth
async def cancel_order(req, uuid):
    session = req.ctx.session
    current_user = req.ctx.current_user

    async with session.begin():
        q = select(Order).where(Order.uuid == uuid)
        try:
            result = await session.execute(q)
            existing_order = result.scalars().one()
        except NoResultFound:
            raise NotFoundException()

        if existing_order.userId != current_user["uuid"]:
            raise BadRequestException("Can't access orders of another user")

        if existing_order.status == OrderStatus.Complete:
            raise BadRequestException("Cannot cancel a completed order")

        await session.execute('UPDATE orders SET status=:status WHERE uuid=:uuid', {'status': OrderStatus.Cancelled, 'uuid': uuid})

    return response.json({"message": "Order is been cancelled"}, status=200)


@order.get("/sellerPaidOrders")
@require_auth
async def get_sellers_paid_products(req):
    session = req.ctx.session
    current_user = req.ctx.current_user

    q = (select(Order)
         .join(OrderProduct, Order.uuid == OrderProduct.orderId)
         .join(Product, OrderProduct.productId == Product.uuid)
         .filter(and_((Order.status == 'complete'), (Product.userId == current_user["uuid"])))
         .options(selectinload(Order.products).selectinload(Product.order_products))
         .group_by(Order.uuid)
         )

    result = await session.execute(q)

    # result = await session.execute('SELECT products.uuid AS products_uuid, products.title AS products_title, products.price AS products_price, products.description AS products_description, products."userId" AS "products_userId", products.version_id AS products_version_id, anon_1.orders_uuid AS anon_1_orders_uuid \
    #     FROM (SELECT orders.uuid AS orders_uuid \
    #     FROM orders JOIN order_products ON orders.uuid = order_products."orderId" \
    #     JOIN products ON products.uuid = order_products."productId" \
    #     WHERE orders.status = :status\
    #     GROUP BY orders.uuid) AS anon_1 \
    #     JOIN order_products AS order_products_1 ON anon_1.orders_uuid = order_products_1."orderId" \
    #     JOIN products ON products.uuid = order_products_1."productId"\
    #     WHERE products."userId" = :userId ', {"status": OrderStatus.Complete, "userId": current_user['uuid']})

    _paidOrders = result.all()

    print('\n\n', _paidOrders, '\n\n')

    res = [order[0].to_dict() for order in _paidOrders]

    print('\n\n', res, '\n\n')

    def filterOrders(order):
        _order = {}
        _order["uuid"] = order["uuid"]
        _order["userId"] = order["userId"]
        _order["status"] = order["status"]
        _order['products'] = list(
            filter(lambda x: x['userId'] == current_user['uuid'], order["products"]))
        return _order

    paidOrders = list(map(filterOrders, res))

    return response.json(paidOrders, status=200)


@order.get("/sellerPaidOrderss")
@require_auth
async def get_sellers_paid_productss(req):
    session = req.ctx.session
    current_user = req.ctx.current_user

    result = await session.execute('\
        SELECT o.*, p.*, op.quantity \
        FROM orders o \
        JOIN order_products op ON o.uuid = op.orderId \
        JOIN products p ON op.productId = p.uuid \
        WHERE p.userId = :userId AND o.status = :status \
    ', {"userId": current_user["uuid"], "status": OrderStatus.Complete})
    _paidOrders = result.all()

    print('\n\n', _paidOrders, '\n\n')

    return response.json({"res": "done"})
