
from flask_restful import Api
from flask_httpauth import HTTPTokenAuth

from app.http.exceptions.base import handle_exception


class ExtendedAPI(Api):
    def handle_error(self, e):
        return handle_exception(e)


# API restful extension
api = ExtendedAPI(prefix='/v1', catch_all_404s=True)

# Authentication extension
auth = HTTPTokenAuth()
