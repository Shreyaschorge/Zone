from marshmallow import Schema, fields, validate


class ProductSchema(Schema):

    title = fields.Str(required=True, validate=[
        validate.Length(max=50, error="Title must be less than 20 characters")])
    price = fields.Float(required=True, validate=[validate.Range(
        min=1, error="Price must be greater than 0")])
    description = fields.Str(required=True, validate=[validate.Length(
        max=100, error="Description cannot exceed 100 characters")])
    uuid = fields.Str()
    userId = fields.Str()
    id = fields.Int()

    class Meta:
        load_only = ("id",)
        dump_only = ("id",)
