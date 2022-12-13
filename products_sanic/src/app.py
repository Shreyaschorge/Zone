import sanic
from sanic import response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from models.product import Product
from db import bind

from contextvars import ContextVar
from zone_common.exceptions import CustomException

from resources.product import product

app = sanic.Sanic(name="product_service")
app.blueprint(product)

_sessionmaker = sessionmaker(bind, AsyncSession, expire_on_commit=False)

_base_model_session_ctx = ContextVar("session")


@app.listener('before_server_start')
async def bst(app, loop):
    async with bind.begin() as conn:
        await conn.run_sync(Product.metadata.create_all)


@app.middleware("request")
async def inject_session(request):
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

    print("log this error", err, type(err))

    if isinstance(err, CustomException):
        return response.json({
            "errors": err.serialize_errors()
        }, status=err.status_code)

    if isinstance(err, Exception):
        return response.json({
            'errors': [{'message': 'Something went wrong'}]
        }, status=500)


if __name__ == "__main__":

    app.run(port=5001, auto_reload=True)
