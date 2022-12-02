from flask_restful import Resource, request
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt
)

from model import UserModel
from schema import UserSchema
from exceptions import BadRequestException, RequestValidationException, DatabaseException

from blocklist import BLOCKLIST

user_schema = UserSchema()
ph = PasswordHasher(memory_cost=32768)


class UserRegister(Resource):
    def post(self):

        try:
            user = user_schema.load(request.get_json())
        except ValidationError as err:
            raise RequestValidationException(err)

        if UserModel.find_by_email(user.email):
            raise BadRequestException('User already exists')

        user.password = ph.hash(user.password)

        try:
            user.save_to_db()
        except:
            raise DatabaseException('An error occurred while creating a user')

        return user_schema.dump(user), 201


class UserLogin(Resource):
    def post(self):

        # Parse and Validate req body
        try:
            user = user_schema.load(request.get_json())
        except ValidationError as err:
            raise RequestValidationException(err)

        # Check if user exists
        existing_user = UserModel.find_by_email(user.email)

        #  if not throw BadRequestException
        if not existing_user:
            raise BadRequestException('Invalid credentials')

        # if user is present verify password
        try:
            ph.verify(existing_user.password, user.password)
        except VerifyMismatchError:
            raise BadRequestException('Invalid credentials')

        # Create JWT payload
        payload = user_schema.dump(existing_user)

        # Create access_token
        access_token = create_access_token(
            identity=payload, fresh=True)

        # Create refresh_token
        refresh_token = create_refresh_token(payload)

        # Check if password rehashing is needed
        if ph.check_needs_rehash(existing_user.password):
            existing_user.password = ph.hash(user.password)
            existing_user.save_to_db()

        # Return access_token and refresh_token
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
