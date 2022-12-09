from ma import ma
from marshmallow import fields, validate

from model.product import ProductModel


class ProductSchema(ma.SQLAlchemyAutoSchema):

    title = fields.Str(required=True, validate=[
        validate.Length(max=50, error="Title must be less than 50 characters")])
    price = fields.Float(required=True, validate=[validate.Range(
        min=1, error="Price must be greater than 0")])
    description = fields.Str(required=True, validate=[validate.Length(
        max=50, error="Description cannot exceed 50 characters")])

    class Meta:
        model = ProductModel
        load_instance = True
        dump_only = ("id",)
        load_only = ("id",)  # Excluded field from res
