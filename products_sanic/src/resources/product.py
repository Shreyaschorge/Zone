from sanic import Blueprint, response
from marshmallow.exceptions import ValidationError
from zone_common.exceptions import RequestValidationException

from models.product import Product
from schema.product import ProductSchema

product = Blueprint(name="product", url_prefix="/api/products")
product_schema = ProductSchema()


@product.get('/')
async def index(req):
    return response.json({"products": "List of products..."})


@product.post("/")
async def create_product(request):
    try:
        _product = product_schema.load(request.json)
        _product["userId"] = "user123"
    except ValidationError as err:
        raise RequestValidationException(err)

    session = request.ctx.session
    async with session.begin():
        product = Product(**_product)
        session.add(product)
    return response.json(product_schema.dump(product.__dict__))
