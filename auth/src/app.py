
import os

from flask import Flask, jsonify
# from flask_restful import Api

from ma import ma
from resources.user import UserRegister
from custom_exceptions.errors import ExtendedAPI

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///data.db')


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


api = ExtendedAPI(app)

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    ma.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5001)
