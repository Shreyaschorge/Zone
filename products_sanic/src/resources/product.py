from sanic import Blueprint, response
from sqlalchemy.future import select
from marshmallow.exceptions import ValidationError
from zone_common.exceptions import RequestValidationException

from models.product import Product
from schema.product import ProductSchema
from middlewares.require_auth import require_auth

product = Blueprint(name="product", url_prefix="/api/products")

product_schema = ProductSchema()
product_list_schema = ProductSchema(many=True)


@product.get('/')
async def index(req):
    session = req.ctx.session
    q = select(Product)
    result = await session.execute(q)
    all_products = product_list_schema.dump(
        result.scalars())
    return response.json(all_products, status=200)


@product.post("/")
@require_auth
async def create_product(req):
    try:
        _product = product_schema.load(req.json)
        _product["userId"] = req.ctx.current_user['uuid']
    except ValidationError as err:
        raise RequestValidationException(err)

    session = req.ctx.session
    async with session.begin():
        product = Product(**_product)
        session.add(product)
    return response.json(product_schema.dump(product.__dict__), status=201)
