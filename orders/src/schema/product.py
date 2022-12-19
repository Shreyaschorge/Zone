from marshmallow import Schema, fields, validate


class ProductSchema(Schema):

    id = fields.Int()
    title = fields.Str()
    price = fields.Float()
    description = fields.Str()
    uuid = fields.Str()
    userId = fields.Str()

    class Meta:
        load_only = ("id",)
        dump_only = ("id",)
