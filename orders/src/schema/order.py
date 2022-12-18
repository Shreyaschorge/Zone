import re
from marshmallow import Schema, fields, validate


class ProductIdField(fields.Field):
    default_error_messages = {
        "invalid": "productId must be valid"
    }

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None

        print('\n\n', value, '\n\n')

        matched = re.match("product_.{30}$", value)

        if not bool(matched):
            self.fail("invalid")

        return value


class OrderSchema(Schema):

    id = fields.Int()
    productId = ProductIdField(required=True)
    uuid = fields.String()

    class Meta:
        load_only = ("id",)
        dump_only = ("id",)
