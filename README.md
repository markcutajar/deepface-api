# Deepface API

The aim of this microservice api is to verify that two images are the same user.

This microservice is served by a simple Flask App with Tensorflow as a backend ML framework

## Set Up

Python version: 3.10.4 (not needed is serving through docker)

In order to ser the flask app up, a `.env` file is needed. An example is provided in `.env.example`. Alternatively you can copy `.env.dev`.

```
# Flask
APP_SETTINGS=app.settings.DevConfig
FLASK_APP=run
FLASK_DEBUG=1
FLASK_ENV=development
```
#### Run without docker
To start the API locally not in a container:
```
flask run
```

#### Run with Docker
To start the API in a container run the following. NOTE: The api will take about 5 mins to start up as it downloads the needed models on initialization. The model weights are not incorporated in the image to preserve image size, but that could be very easily done too instead.
```
docker-compose up -d --build
docker-compose -f development.yml up -d --build
docker-compose -f production.yml up -d --build
```

## Endpoints
```
curl --location --request POST 'http://127.0.0.1:5000/v1/actions/verify' \
--header 'Content-Type: application/json' \
--data-raw '{
    "images": [
		{
            "image1": "<image base64 starting with data:image/... goes here>",
            "image1": "<image base64 starting with data:image/... goes here>"
        }
    ]
}'
```

Other top level optional parameters:
```
{
    "model": <VGG-Face, Facenet, OpenFace, DeepFace, DeepID, Dlib, ArcFace or Ensemble>, // ONLY VGG-Face and Facenet are preloaded
    "distance_metric": <cosine, euclidean, euclidean_l2>,
    "detector_backend": <retinaface, mtcnn, opencv, ssd or dlib>,
}
```
