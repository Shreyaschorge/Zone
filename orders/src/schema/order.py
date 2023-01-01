import re
from marshmallow import Schema, fields, validate


class ProductIdField(fields.Field):
    default_error_messages = {
        "invalid": "productId must be valid"
    }

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None

        matched = re.match("product_.{30}$", value)

        if not bool(matched):
            self.fail("invalid")

        return value


class OrderSchema(Schema):

    products = fields.List(ProductIdField(required=True))
    status = fields.String()
    uuid = fields.String()

    class Meta:
        load_only = ("products")
