import functools
import hashlib
import json
import math
import urllib

from flask import request
from werkzeug.exceptions import BadRequest


def get_request_json(req):
    try:
        if not req.is_json:
            raise BadRequest()
        return req.json
    except BadRequest:
        raise BadRequest(f"Incorrect json body received. Expected json. Got {req.data[:300]}")


def make_cache_key():
    body = json.dumps(get_request_json(request), separators=(",", ":"))
    args = (
        request.path
        + "?"
        + urllib.parse.urlencode([(k, v) for k in sorted(request.args) for v in sorted(request.args.getlist(k))])
    )
    key = args + body
    return hashlib.md5(key.encode("utf-8")).hexdigest()


def paginator(collection="items", many=False, max_per_page=2500):
    """Generate a paginated response for a resource collection.
    Routes that use this decorator must return a SQLAlchemy query as a
    response.
    The output of this decorator is a Python dictionary with the paginated
    results. The application must ensure that this result is converted to a
    response object, either by chaining another decorator or by using a
    custom response object that accepts dictionaries."""

    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            query, schema, extra_params = f(*args, **kwargs)

            page = request.args.get("page", 1, type=int)
            per_page = min(request.args.get("perPage", max_per_page, type=int), max_per_page)

            if isinstance(query, list):
                items = query[per_page * (page - 1) : (per_page * page)]
                total_results = len(query)
                total_pages = math.ceil(total_results / per_page)
            else:
                p = query.paginate(page, per_page, error_out=False)
                items = p.items
                total_results = query.count()
                total_pages = p.pages

            pages = {
                "currentPage": page,
                "perPage": per_page,
                "totalPages": total_pages,
                "totalRecords": total_results,
            }
            results = schema.dump(items, many=many)
            response = {collection: results, "paging": pages}

            if isinstance(extra_params, dict):
                for k, v in extra_params.items():
                    response[k] = v
            return response

        return wrapped

    return decorator