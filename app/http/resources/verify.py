"""Verify api functions"""
import uuid
import time
from flask import request
from flask_restful import Resource

from app.http.utils import get_request_json
from app.http.exceptions.base import InvalidRequestObject
from app.services.verify import ImageVerify


class Verify(Resource):
    def post(self):
        start = time.time()
        request_json = get_request_json(request)
        request_id = str(uuid.uuid4())

        model = request_json.get('model')
        distance_metric = request_json.get('distance_metric')
        detector_backend = request_json.get('detector_backend')
        images = request_json.get('images')
        if not isinstance(images, list):
            raise InvalidRequestObject('images key expected to be a list of pairs with image1 and image2')

        image_verifier = ImageVerify(model, distance_metric, detector_backend)
        result = image_verifier.verify(images)

        result["request_id"] = request_id
        result["request_duration"] = round((time.time() - start) * 1000)
        return result
