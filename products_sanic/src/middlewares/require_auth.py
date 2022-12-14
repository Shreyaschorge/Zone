from functools import wraps
from sanic.request import Request

from zone_common.exceptions import UnauthorizedException


def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwa):

        print('\n\n', args[0].ctx.current_user, '\n\n')
        if not args[0].ctx.current_user:
            raise UnauthorizedException()

        return f(*args, **kwa)
    return decorated_function
