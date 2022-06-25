


import json
import traceback
from http import HTTPStatus

from flask import Response, current_app
from werkzeug.exceptions import BadRequest, HTTPException


def register_exception_handling(app):
    @app.errorhandler(Exception)
    def handler(e):
        handle_exception(e)


def handle_exception(e):
    current_app.logger.error(e)
    if current_app.config["DEBUG"]:
        traceback.print_exc()
    response = e.get_response() if isinstance(e, HTTPException) else Response()
    code = getattr(e, "code", 500)
    response.data = json.dumps(
        {
            "code": code,
            "name": getattr(e, "error_name", getattr(e, "name", e.__class__.__name__)),
            "description": getattr(e, "description", str(e)),
            "detail": e.data if hasattr(e, "data") else None,
        }
    )
    response.content_type = "application/json"

    if not isinstance(code, (str, bytes, int, HTTPStatus)):
        response.status_code = 500
    else:
        response.status_code = code
    return response


class BaseExceptionMixin(Exception):
    def __init__(self, description=None, name=None, data=None):
        self.error_name = name if name is not None else self.__class__.__name__
        self.data = data
        if description is not None:
            self.description = description


class InvalidRequestObject(BadRequest, BaseExceptionMixin):
    description = "Invalid request object"
    code = 422


class NotBase64Image(InvalidRequestObject):
    description = "Image provided is not base 64"
    code = 400


class NothingToProcess(InvalidRequestObject):
    description = "No images are provided to process"
    code = 400