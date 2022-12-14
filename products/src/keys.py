import os

PG_USER = os.environ.get('PG_USER')
PG_HOST = os.environ.get('PG_HOST')
PG_PORT = os.environ.get('PG_PORT')
PG_DATABASE = os.environ.get('PG_DATABASE')
PG_PASSWORD = os.environ.get('PG_PASSWORD')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_ALGORITHM = 'HS256'
