import asyncio as aio
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
from events.order_created_publisher import OrderCreatedPublisher
from events.order_cancelled_publisher import OrderCancelledPublisher
from natsWrapper import natsWrapper

order = Blueprint(name="order", url_prefix="/api/orders")


@order.get("/test")
async def test_route(req):
    return response.text("Hi 😎")


@order.get('/')
@require_auth
async def all_users_orders(req):
    session = req.ctx.session
    userId = req.ctx.current_user["uuid"]
    async with session.begin():
        q = (select(Order)
             .join(OrderProduct, Order.uuid == OrderProduct.orderId)
             .join(Product, OrderProduct.productId == Product.uuid)
             .filter(Order.userId == userId)
             .options(selectinload(Order.products)
                      .selectinload(Product.order_products)).group_by(Order.uuid))

        result = await session.execute(q)
        all_orders = result.scalars().all()

    return response.json([order.to_orderProducts_dict() for order in all_orders], status=200)


@order.get("/<uuid>")
@require_auth
async def single_order(req, uuid):
    session = req.ctx.session
    async with session.begin():

        qu = (select(Order).where(Order.uuid == uuid)
              .options(selectinload(Order.products).selectinload(Product.order_products))
              )

        result = await session.execute(qu)
        existing_order = result.scalars().first()

    if existing_order.userId != req.ctx.current_user["uuid"]:
        raise BadRequestException("Can't access orders of another user")

    return response.json(existing_order.to_orderProducts_dict(), status=200)


@order.post('/')
@require_auth
async def create_order(req):

    session = req.ctx.session
    current_user = req.ctx.current_user
    payload = req.json
    total_price = 0

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

        order = Order()
        order.userId = current_user["uuid"]
        session.add(order)

        order_products = []

        for product in existing_products:
            total_price = total_price + \
                (product.price * getProductQuantity(product))
            order_products.append(OrderProduct(
                order=order, product=product, quantity=getProductQuantity(product)))

        for order_product in order_products:
            session.add(order_product)

        await session.commit()

    # Build order to be published
    _order = {
        "uuid": order.uuid,
        "price": total_price,
        "userId": order.userId,
        "status": order.status
    }
    # Publish order created event
    aio.create_task(OrderCreatedPublisher(natsWrapper.client).publish(_order))

    return response.json({"uuid": order.uuid}, status=201)


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

        if existing_order.status == OrderStatus.Completed:
            raise BadRequestException("Cannot cancel a completed order")

        existing_order.status = OrderStatus.Cancelled
        session.add(existing_order)
        await session.commit()

    #  Publish order cancalled event
    aio.create_task(OrderCancelledPublisher(
        natsWrapper.client).publish({
            "uuid": existing_order.uuid,
            "version_id": existing_order.version_id
        }))

    return response.json({"message": "Order is been cancelled"}, status=200)


@order.get("/soldProducts")
@require_auth
async def get_sellers_paid_products(req):
    session = req.ctx.session
    current_user = req.ctx.current_user

    q = (select(Order)
         .join(OrderProduct, Order.uuid == OrderProduct.orderId)
         .join(Product, OrderProduct.productId == Product.uuid)
         .filter(and_(Order.status == OrderStatus.Completed, Order.userId != current_user["uuid"]))
         .options(selectinload(Order.products.and_(Product.userId == current_user["uuid"]))
         .selectinload(Product.order_products))
         .group_by(Order.uuid)
         )

    result = await session.execute(q)
    _paidOrders = result.all()

    return response.json([order[0].to_orderProducts_dict() for order in _paidOrders], status=200)
