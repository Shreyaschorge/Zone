import os
from app import app
from db import db
from ma import ma

if (os.environ.get('PG_USER') is None):
    raise Exception('PG_USER must be defined')

if (os.environ.get('PG_HOST') is None):
    raise Exception('PG_HOST must be defined')

if (os.environ.get('PG_PORT') is None):
    raise Exception('PG_PORT must be defined')

if (os.environ.get('PG_DATABASE') is None):
    raise Exception('PG_DATABASE must be defined')

if (os.environ.get('PG_PASSWORD') is None):
    raise Exception('PG_PASSWORD must be defined')

if (os.environ.get('REDIS_URI') is None):
    raise Exception('REDIS_URI must be defined')

if (os.environ.get('JWT_SECRET_KEY') is None):
    raise Exception('JWT_SECRET_KEY must be defined')

db.init_app(app)
ma.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


app.run(host='0.0.0.0', port=3000)
