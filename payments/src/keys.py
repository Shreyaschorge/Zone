import os
from decouple import config

STRIPE_SECRET = os.environ.get('STRIPE_SECRET', config('STRIPE_SECRET'))