from flask_restful import Resource, request
from argon2 import PasswordHasher
from marshmallow.exceptions import ValidationError

from model import UserModel
from schema import UserSchema
from exceptions import BadRequestException, RequestValidationException, DatabaseException

user_schema = UserSchema()
ph = PasswordHasher()


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

        return {"message": "User created successfully."}, 201
