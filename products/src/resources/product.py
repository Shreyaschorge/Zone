import asyncio as aio
from sanic import Blueprint, response
from sqlalchemy.future import select
from sqlalchemy.orm.exc import NoResultFound
from marshmallow.exceptions import ValidationError
from zone_common.exceptions import RequestValidationException, NotFoundException, UnauthorizedException, BadRequestException
from zone_common.middlewares.require_auth import require_auth

from models.product import Product
from schema.product import ProductSchema
from events.product_created_publisher import ProductCreatedPublisher
from natsWrapper import natsWrapper

product = Blueprint(name="product", url_prefix="/api/products")

product_schema = ProductSchema()
product_list_schema = ProductSchema(many=True)


@product.get('/')
async def all_products(req):
    session = req.ctx.session
    q = select(Product)
    result = await session.execute(q)
    all_products = product_list_schema.dump(
        result.scalars())
    return response.json(all_products, status=200)


@product.get('/<uuid>')
async def single_product(req, uuid):
    session = req.ctx.session
    q = select(Product).where(Product.uuid == uuid)

    try:
        result = await session.execute(q)
        existing_product = result.scalars().one()
    except NoResultFound as err:
        raise NotFoundException()

    product = product_schema.dump(existing_product)
    return response.json(product, status=200)


@product.post("/")
@require_auth
async def create_product(req):
    try:
        _product = product_schema.load(req.json)
        _product['userId'] = req.ctx.current_user['uuid']
    except ValidationError as err:
        raise RequestValidationException(err)

    session = req.ctx.session
    async with session.begin():
        product = Product(**_product)
        session.add(product)

    parsedProduct = product_schema.dump(product.__dict__)
    aio.create_task(ProductCreatedPublisher(
        natsWrapper.client).publish(parsedProduct))
    return response.json(parsedProduct, status=201)


@product.put("/<uuid>")
@require_auth
async def update_product(req, uuid):
    session = req.ctx.session
    q = select(Product).where(Product.uuid == uuid)

    try:
        result = await session.execute(q)
        existing_product = result.scalars().one()
    except NoResultFound as err:
        raise NotFoundException()

    if existing_product.userId != req.ctx.current_user['uuid']:
        raise BadRequestException(
            "Not allowed to update someone's else product")

    try:
        product = product_schema.load(req.json)
    except ValidationError as err:
        raise RequestValidationException(err)

    existing_product.title = product["title"]
    existing_product.description = product["description"]
    existing_product.price = product["price"]

    session.add(existing_product)
    await session.commit()

    return response.json(product_schema.dump(existing_product), status=200)


@product.get("/usersProducts")
@require_auth
async def users_products(req):

    userId = req.ctx.current_user["uuid"]

    session = req.ctx.session
    q = select(Product).where(Product.userId == userId)
    result = await session.execute(q)
    all_users_products = product_list_schema.dump(
        result.scalars())

    return response.json(all_users_products, status=200)
