import re
from marshmallow import Schema, fields


class OrderIdField(fields.Field):
    default_error_messages = {
        "invalid": "orderId must be valid"
    }

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None

        matched = re.match("order_.{30}$", value)

        if not bool(matched):
            self.fail("invalid")

        return value


class PaymentSchema(Schema):
    orderId = OrderIdField(required=True)
    token = fields.Str(required=True)
