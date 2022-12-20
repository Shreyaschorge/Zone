import os
from sanic import Blueprint, response
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm.exc import NoResultFound
from zone_common.exceptions import RequestValidationException, NotFoundException, BadRequestException
from zone_common.middlewares.require_auth import require_auth
from zone_common.events.order_status import OrderStatus
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.order import Order, order_product
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

    async with session.begin():
        try:
            payload = order_schema.load(req.json)
        except ValidationError as err:
            raise RequestValidationException(err)

        q = select(Product).filter(Product.uuid.in_(
            e for e in payload["products"]))

        result = await session.execute(q)
        existing_products = result.scalars().all()

        if len(existing_products) != len(payload["products"]):
            raise NotFoundException()

        order = Order(products=existing_products)
        order.userId = current_user["uuid"]
        session.add(order)
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
