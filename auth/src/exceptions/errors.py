from flask import jsonify
from flask_restful import Api

from exceptions import CustomException


class ExtendedAPI(Api):
    """
        This class overrides 'handle_error' method of 'Api' class from flask-restful.
    """

    def handle_error(self, err):

        # TODO - Implement logging

        print("log this error", err, type(err))

        if isinstance(err, CustomException):
            return jsonify({
                "errors": err.serialize_errors()
            }), err.status_code

        return jsonify(**err.kwargs), err.http_status_code
