import os
from decouple import config

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", config('JWT_SECRET_KEY'))
