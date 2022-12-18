from sanic import Blueprint, response
from sqlalchemy import select
from marshmallow.exceptions import ValidationError
from zone_common.exceptions import RequestValidationException

from models.order import Order
from schema.order import OrderSchema

order = Blueprint(name="order", url_prefix="/api/orders")

order_schema = OrderSchema()


@order.get('/')
async def all_orders(req):
    session = req.ctx.session
    async with session.begin():
        q = select(Order)
        result = await session.execute(q)
        all_orders = result.scalars()

        return response.json([order.to_json() for order in all_orders])


@order.post('/')
async def create_order(req):

    try:
        payload = order_schema.load(req.json)
    except ValidationError as err:
        raise RequestValidationException(err)

    print('\n\n', payload, '\n\n')

    session = req.ctx.session
    async with session.begin():
        order = Order(**payload)
        session.add(order)

    return response.json({"message": "Order is created"})
