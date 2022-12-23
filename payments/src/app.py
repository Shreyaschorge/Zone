from sanic import Sanic

from constants import APP_NAME
from resources.payment import payment

app = Sanic(name=APP_NAME)
app.blueprint(payment)
