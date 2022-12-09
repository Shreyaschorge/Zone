from flask_restful import request
from functools import wraps

from zone_common.exceptions import UnauthorizedException


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not request.environ.get("current_user"):
            raise UnauthorizedException()

        return f(*args, **kws)
    return decorated_function
