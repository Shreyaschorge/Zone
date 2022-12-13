from sanic import Blueprint, response

product = Blueprint(name="product", url_prefix="/api/products")


@product.get('/')
async def index(req):
    return response.json({"products": "List of products..."})
