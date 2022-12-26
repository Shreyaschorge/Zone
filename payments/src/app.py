
from sanic import Sanic, response
from contextvars import ContextVar
from zone_common.middlewares.current_user import current_user
from zone_common.exceptions import CustomException

from db import bind, _sessionmaker
from models.order import Order
from models.payment import Payment
from resources.payment import payment
from natsWrapper import natsWrapper

from constants import APP_NAME
from keys import NATS_URL

app = Sanic(name=APP_NAME)
app.blueprint(payment)

_base_model_session_ctx = ContextVar("session")


@app.listener('before_server_start')
async def before_start(app, loop):
    try:

        await natsWrapper.connect(url=NATS_URL)

        async with bind.begin() as conn:
            await conn.run_sync(Order.metadata.create_all)
            await conn.run_sync(Payment.metadata.create_all)
            await conn.commit()

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

    print(f"{APP_NAME} error", err, type(err))

    if isinstance(err, CustomException):
        return response.json({
            "errors": err.serialize_errors()
        }, status=err.status_code)

    if isinstance(err, Exception):
        return response.json({
            'errors': [{'message': 'Something went wrong'}]
        }, status=500)
