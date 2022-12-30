import os
from app import app

if (os.environ.get('NATS_URL') is None):
    raise Exception('NATS_URL must be defined')

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

if (os.environ.get('JWT_SECRET_KEY') is None):
    raise Exception('JWT_SECRET_KEY must be defined')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000,  dev=True,)
