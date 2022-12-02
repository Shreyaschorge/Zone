from ma import ma
from marshmallow import fields, validate

from model.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):

    email = fields.Str(required=True, validate=[
        validate.Email(error="Please provide valid email")])
    password = fields.Str(required=True, validate=[validate.Length(
        min=11, max=25, error="Password length must be between 11-25 characters")])

    class Meta:
        model = UserModel
        load_instance = True
        dump_only = ("id",)
        load_only = ("password", "id")  # Excluded field from res
