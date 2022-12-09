import os

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from ma import ma
from resources.user import UserRegister, UserLogin, UserLogout, TokenRefresh
from extended_api import ExtendedAPI
from blocklist import jwt_redis_blocklist

from keys import JWT_SECRET_KEY, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

api = ExtendedAPI(app)
jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jwt_redis_blocklist.get(jti) is not None


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "errors": [{"message": "Token Expired"}]
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "errors": [{"message": "Signature verification failed. Invalid Token."}]
    }), 401


@jwt.token_verification_failed_loader
def token_verification_failed(jwt_header, jwt_payload):
    return jsonify({
        "errors": [{"message": "Token verification failed"}]
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "errors": [{"message": "Missing token in the request"}]
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return jsonify({
        "errors": [{"message": "Token is not fresh"}]
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "errors": [{"message": "Token has been revoked"}]
    }), 401


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


api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
