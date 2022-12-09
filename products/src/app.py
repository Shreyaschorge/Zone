from flask import Flask, jsonify

from extended_api import ExtendedAPI
from resources.product import Product, ProductList, UsersProduct
from middleware.current_user import current_user

app = Flask(__name__)

app.before_request_funcs = {
    None: [current_user]
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['PROPAGATE_EXCEPTIONS'] = True

api = ExtendedAPI(app)


@app.errorhandler(Exception)
def handle_error(err):
    """
        Final exception handler middleware in the chain.
    """

    # TODO Log this too
    print('\n\n', err, '\n\n')

    if isinstance(err, Exception):
        return jsonify({
            'errors': [{'message': 'Something went wrong'}]
        }), 500


api.add_resource(Product, '/api/products/<uuid>')
api.add_resource(ProductList, '/api/products')
api.add_resource(UsersProduct, '/api/products/usersProducts')
