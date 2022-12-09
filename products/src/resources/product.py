from flask_restful import Resource, request
from marshmallow.exceptions import ValidationError
from zone_common.exceptions import RequestValidationException, DatabaseException

from schema.product import ProductSchema

product_schema = ProductSchema()


class Product(Resource):
    def get(self, uuid):
        return f'Here is ur get product {uuid}', 200

    def put(self, uuid):
        return f'Here is ur put product {uuid}', 200

    def delete(self, uuid):
        return 'Product deleted', 200


class ProductList(Resource):
    def get(self):
        return 'Product List', 200
        pass

    def post(self):

        try:
            product = product_schema.load(request.get_json())
            product.userId = "User123"
        except ValidationError as err:
            raise RequestValidationException(err)

        try:
            product.save_to_db()
        except:
            raise DatabaseException('An error occurred while creating product')

        return product_schema.dump(product), 201
