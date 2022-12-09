from flask_restful import Resource, request
from marshmallow.exceptions import ValidationError
from zone_common.exceptions import (
    RequestValidationException,
    NotFoundException,
    UnauthorizedException,
    BadRequestException
)

from schema.product import ProductSchema
from middleware.require_auth import require_auth
from model.product import ProductModel

product_schema = ProductSchema()
product_list_schema = ProductSchema(many=True)
users_product_schema = ProductSchema(many=True)


class Product(Resource):

    @require_auth
    def get(self, uuid):
        existing_product = ProductModel.find_by_uuid(uuid)

        if not existing_product:
            raise NotFoundException()

        return product_schema.dump(existing_product), 200

    @require_auth
    def put(self, uuid):
        existing_product = ProductModel.find_by_uuid(uuid)
        if not existing_product:
            raise NotFoundException()

        current_user = request.environ.get("current_user")
        if existing_product.userId != current_user["uuid"]:
            raise UnauthorizedException()

        try:
            product = product_schema.load(request.get_json())
        except ValidationError as err:
            raise RequestValidationException(err)

        existing_product.title = product.title
        existing_product.description = product.description
        existing_product.price = product.price

        existing_product.save_to_db()

        return product_schema.dump(existing_product), 200


class ProductList(Resource):

    def get(self):
        all_products = ProductModel.find_all()
        return product_list_schema.dump(all_products), 200

    @require_auth
    def post(self):
        try:
            product = product_schema.load(request.get_json())
            current_user = request.environ.get("current_user")
            product.userId = current_user["uuid"]
        except ValidationError as err:
            raise RequestValidationException(err)

        product.save_to_db()

        return product_schema.dump(product), 201


class UsersProduct(Resource):

    @require_auth
    def get(self):
        current_user = request.environ.get("current_user")
        usersProducts = ProductModel.find_user_products(current_user["uuid"])
        return users_product_schema.dump(usersProducts), 200
