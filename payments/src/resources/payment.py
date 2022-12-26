import asyncio as aio
from sanic import Blueprint, response
from zone_common.middlewares.require_auth import require_auth
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm.exc import NoResultFound
from zone_common.exceptions import RequestValidationException, NotFoundException, BadRequestException
from zone_common.events.order_status import OrderStatus
from sqlalchemy.future import select

from models.order import Order
from models.payment import Payment
from schema.payment import PaymentSchema
from stripeClient import stripe
from events.payment_created_publisher import PaymentCreatedPublisher
from natsWrapper import natsWrapper

payment = Blueprint(name="payment", url_prefix="/api/payments")

payment_schema = PaymentSchema()


@payment.post('/')
@require_auth
async def create_charge(req):
    session = req.ctx.session
    userId = req.ctx.current_user["uuid"]

    try:
        order = payment_schema.load(req.json)
    except ValidationError as err:
        raise RequestValidationException(err)

    q = select(Order).where(Order.uuid == order['orderId'])

    async with session.begin():
        try:
            result = await session.execute(q)
            existing_order = result.scalars().one()
        except NoResultFound as err:
            raise NotFoundException()

        if existing_order.userId != userId:
            raise BadRequestException("Can't access orders of another user")

        if existing_order.status == OrderStatus.Cancelled:
            raise BadRequestException("Can't pay for cancalled order")

        if existing_order.status == OrderStatus.Completed:
            raise BadRequestException("Can't pay for paid order")

        charge = stripe.Charge.create(amount=int(existing_order.price * 100), currency='inr',
                                      source=order['token'], metadata={"userId": userId})

        _payment = {
            "orderId": existing_order.uuid,
            "chargeId": charge.id
        }
        payment = Payment(**_payment)
        session.add(payment)

        existing_order.status = OrderStatus.Completed
        session.add(existing_order)

        await session.commit()

    # Publish payment created event
    aio.create_task(PaymentCreatedPublisher(natsWrapper.client).publish({
        "uuid": payment.uuid,
        "orderId": existing_order.uuid,
        "version_id": existing_order.version_id
    }))

    return response.json({"id": payment.uuid})
