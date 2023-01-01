import os
from decouple import config

NATS_URL = os.environ.get('NATS_URL', config('NATS_URL'))
PG_USER = os.environ.get('PG_USER', config('PG_USER'))
PG_HOST = os.environ.get('PG_HOST', config('PG_HOST'))
PG_PORT = os.environ.get('PG_PORT', config('PG_PORT'))
PG_DATABASE = os.environ.get('PG_DATABASE', config('PG_DATABASE'))
PG_PASSWORD = os.environ.get('PG_PASSWORD', config('PG_PASSWORD'))