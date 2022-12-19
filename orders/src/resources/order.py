from sanic import Blueprint, response
from marshmallow.exceptions import ValidationError
from zone_common.exceptions import RequestValidationException, NotFoundException
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.order import Order
from models.product import Product
from schema.order import OrderSchema

order = Blueprint(name="order", url_prefix="/api/orders")

order_schema = OrderSchema()


@order.get('/')
async def all_orders(req):
    session = req.ctx.session
    async with session.begin():
        q = select(Order).options(
            selectinload(Order.products))
        result = await session.execute(q)
        all_orders = result.scalars().all()

    return response.json([order.to_dict() for order in all_orders])


@order.post('/')
async def create_order(req):

    session = req.ctx.session

    try:
        payload = order_schema.load(req.json)
    except ValidationError as err:
        raise RequestValidationException(err)

    q = select(Product).filter(Product.uuid.in_(
        e for e in payload["products"]))

    try:
        result = await session.execute(q)
        existing_products = result.scalars().all()
    except Exception as err:
        raise Exception("Something went wrong", err)

    if len(existing_products) != len(payload["products"]):
        raise NotFoundException()

    order = Order(products=existing_products)
    session.add(order)
    await session.commit()

    return response.json({"message": "Order is created"})
