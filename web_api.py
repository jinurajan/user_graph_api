import logging
from flask import Flask, request, jsonify
from flask_restful import Api

from api.user import (
    UserListHandler,
    UserHandler)
from api.following_users import (
    FollowUserListHandler,
    FollowUserHandler)
from common.errors import *
from common.constants import StatusCode
from conf.settings import Config

log = logging.getLogger(__name__)


def user_api_error_handler(exception):
    '''
    This is one catch exception log error for all exceptions handled
    This logs
        1. Exception Class
        2. Request Method (GET, POST, PUT, DELETE)
        3. Request Path (Helps to find which API was invoked)
        4. XHR status (Whether request is Ajax request or regular)
        5. Arguments (its a dict with 2 keys q and p.
            - q holds a dict of query arguments
            - p holds a dict of form arguments. This is empty for GET requests.

    When a PermissionError is encountered, we send a 403 to FrontEnd
    For all known AthenaErrors, we send a 409
    For all unexpected exceptions, we send a true 500
    '''
    log.exception(
        "[%s] %s to %s - XHR: %s, Args: %s", exception.__class__.__name__,
        request.method, request.path, request.is_xhr,
        {"q": request.args.to_dict(), "p": request.form.to_dict()}
    )
    error_message = exception.args[0]
    error_extra = {}
    if hasattr(exception, 'extra'):
        error_extra = exception.extra

    if isinstance(exception, BadRequestError):
        return jsonify(message=error_message, extra=error_extra), StatusCode.STATUS_BAD_REQUEST
    elif isinstance(exception, PermissionError):
        return jsonify(message=error_message, extra=error_extra), StatusCode.STATUS_PERMISSION_ERROR
    elif isinstance(exception, NotFoundError):
        return jsonify(message=error_message, extra=error_extra), StatusCode.STATUS_NOT_FOUND
    elif isinstance(exception, NotAllowedError):
        return jsonify(message=error_message, extra=error_extra), StatusCode.STATUS_NOT_ALLOWED
    elif isinstance(exception, NotImplementedError):
        return jsonify(message=error_message, extra=error_extra), StatusCode.STATUS_NOT_IMPLEMENTED
    elif isinstance(exception, ConflictError):
        return jsonify(message=error_message, extra=error_extra), StatusCode.STATUS_CONFLICT_ERROR
    else:
        return jsonify(message=error_message, extra=error_extra), StatusCode.STATUS_INTERNAL_SERVER_ERROR

app = Flask(__name__)
app.errorhandler(Exception)(user_api_error_handler)

api = Api(app)

api.add_resource(UserListHandler, '/users')
api.add_resource(UserHandler, '/users/<email>')
api.add_resource(FollowUserListHandler, '/users/<email>/following_users')
api.add_resource(FollowUserHandler, '/users/<email>/following_users/<following_user_email>')


@app.after_request
def set_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = request.headers.get(
        'Origin', '*')

    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS'
        response.headers['Access-Control-Max-Age'] = '3600'  # 1 hour cache
    return response


if __name__ == '__main__':
    app.run(debug=True, port=Config.port)
