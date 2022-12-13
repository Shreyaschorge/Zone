import sanic
from sanic import response

from resources.product import product

app = sanic.Sanic(name="product_service")
app.blueprint(product)


if __name__ == "__main__":
    app.run(port=8000, auto_reload=True)
