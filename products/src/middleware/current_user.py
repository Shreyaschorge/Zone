from flask_restful import request
import jwt
from zone_common.exceptions import UnauthorizedException

from keys import JWT_ALGORITHM, JWT_SECRET_KEY


def current_user():

    if request.headers.get('Authorization'):
        bearer_token = request.headers.get('Authorization')
        token = bearer_token.split()[1]

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, JWT_ALGORITHM)
            request.environ["current_user"] = payload['sub']
        except:
            raise UnauthorizedException()
