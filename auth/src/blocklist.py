import os
import redis
from keys import REDIS_URI

jwt_redis_blocklist = redis.from_url(REDIS_URI)
