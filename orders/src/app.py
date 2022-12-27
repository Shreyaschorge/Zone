import asyncio as aio
from sanic import Sanic, response
from zone_common.exceptions import CustomException
from zone_common.middlewares.current_user import current_user
from contextvars import ContextVar
from sanic_cors import CORS

from db import bind, _sessionmaker
from resources.order import order
from models.order import Order
from models.product import Product
from models.order_products import OrderProduct
from events.product_created_listner import ProductCreatedListner
from events.product_updated_listner import ProductUpdatedListner
from events.payment_created_listener import PaymentCreatedListener
from natsWrapper import natsWrapper

from constants import APP_NAME
from keys import NATS_URL

app = Sanic(name=APP_NAME)
CORS(app)
app.blueprint(order)

_base_model_session_ctx = ContextVar("session")


@app.listener('before_server_start')
async def bst(app, loop):
    try:
        await natsWrapper.connect(url=NATS_URL)

        async with bind.begin() as conn:
            await conn.run_sync(Product.metadata.create_all)
            await conn.run_sync(Order.metadata.create_all)
            await conn.run_sync(OrderProduct.metadata.create_all)
            await conn.commit()

        aio.create_task(ProductCreatedListner(natsWrapper.client).listen())
        aio.create_task(ProductUpdatedListner(natsWrapper.client).listen())
        aio.create_task(PaymentCreatedListener(natsWrapper.client).listen())
    except Exception as err:
        print(f'Error => : {APP_NAME}', err)


@app.middleware("request")
async def inject_session_and_verify_user(request):

    current_user(request=request)

    request.ctx.session = _sessionmaker()
    request.ctx.session_ctx_token = _base_model_session_ctx.set(
        request.ctx.session)


@app.middleware("response")
async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(request.ctx.session_ctx_token)
        await request.ctx.session.close()


@app.exception(Exception)
async def catch_anything(request, err):

    print("order_service error", err, type(err))

    if isinstance(err, CustomException):
        return response.json({
            "errors": err.serialize_errors()
        }, status=err.status_code)

    if isinstance(err, Exception):
        return response.json({
            'errors': [{'message': 'Something went wrong'}]
        }, status=500)
