
import jwt
from zone_common.exceptions import UnauthorizedException

from keys import JWT_ALGORITHM, JWT_SECRET_KEY


def current_user(request):
    if request.headers.get('authorization'):
        bearer_token = request.headers.get('authorization')
        token = bearer_token.split()[1]

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
            request.ctx.current_user = payload['sub']
        except:
            raise UnauthorizedException()
