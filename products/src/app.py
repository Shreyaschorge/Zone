import sanic
from sanic import response
from zone_common.exceptions import CustomException
from contextvars import ContextVar

from resources.product import product
from models.product import Product
from db import bind, _sessionmaker

from middlewares.current_user import current_user

app = sanic.Sanic(name="product_service")
app.blueprint(product)

_base_model_session_ctx = ContextVar("session")


@app.listener('before_server_start')
async def bst(app, loop):
    async with bind.begin() as conn:
        await conn.run_sync(Product.metadata.create_all)


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

    print("product_service error", err, type(err))

    if isinstance(err, CustomException):
        return response.json({
            "errors": err.serialize_errors()
        }, status=err.status_code)

    if isinstance(err, Exception):
        return response.json({
            'errors': [{'message': 'Something went wrong'}]
        }, status=500)

