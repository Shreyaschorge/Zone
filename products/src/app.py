from flask import Flask


from extended_api import ExtendedAPI
from resources.product import Product, ProductList

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['PROPAGATE_EXCEPTIONS'] = True

api = ExtendedAPI(app)

api.add_resource(Product, '/api/products/<uuid>')
api.add_resource(ProductList, '/api/products')
