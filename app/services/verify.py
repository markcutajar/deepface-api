

from deepface import DeepFace

from app.http.exceptions.base import NotBase64Image, NothingToProcess


class ImageVerify:

    # Make sure these are lower case
    models = ['vgg-face']
    distance_metrics = ['cosine']
    detector_backends = ['opencv']

    def __init__(self, model=None, distance_metric=None, detector_backend=None):
        self.model = model or 'VGG-Face' 
        self.distance_metric = distance_metric or 'cosine'
        self.detector_backend = detector_backend or 'opencv'
   

        self.verify_model(self.model)
        self.verify_distance_metric(self.distance_metric)
        self.verify_detector_backend(self.detector_backend)

    @classmethod
    def verify_model(cls, model):
        return cls._is_in_list(model, cls.models)

    @classmethod
    def verify_distance_metric(cls, distance_metric):
        return cls._is_in_list(distance_metric, cls.distance_metrics)

    @classmethod
    def verify_detector_backend(cls, detector_backend):
        return cls._is_in_list(detector_backend, cls.detector_backends)

    @staticmethod
    def _is_in_list(item, list_):
        if item.lower() in list_:
            return True
        return False

    @staticmethod
    def _is_base64_image(image):
        # TODO: Needs better verification
        if image is not None and len(image) > 11 and image[0:11] == "data:image/":
            return True
        return False
    
    @classmethod
    def _check_pair(cls, pair):
        image1 = pair.get('image1')
        if not cls._is_base64_image(image1):
            raise NotBase64Image('Image provided for image1 is not base64. Expected to start with data:image/')

        image2 = pair.get('image2')
        if not cls._is_base64_image(image2):
            raise NotBase64Image('Image provided for image2 is not base64. Expected to start with data:image/')
        return [image1, image2]
    
    def verify(self, pairs):
        
        to_process = [self._check_pair(pair) for pair in pairs]
        if len(to_process) == 0:
            raise NothingToProcess()
        
        try:
            result = DeepFace.verify(
                to_process,
                model_name=self.model,
                distance_metric=self.distance_metric,
                detector_backend=self.detector_backend,
                prog_bar=False
            )

            if self.model == "Ensemble":
                for key in result:
                    result[key]['verified'] = bool(result[key]['verified'])

        except Exception as err:
            # TODO: Handle better here
            raise

        return result
