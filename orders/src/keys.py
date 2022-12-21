import os
from decouple import config

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", config('JWT_SECRET_KEY'))
NATS_URL = os.environ.get('NATS_URL', config('NATS_URL'))