from flask_restful import Resource, request


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
        return 'Add product', 201
