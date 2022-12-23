from sanic import Blueprint, response

payment = Blueprint(name="payment", url_prefix="/api/payments")


@payment.get('/')
async def index(req):
    return response.json({"Hello": "I am working...!!!"})
