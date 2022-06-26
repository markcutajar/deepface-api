FROM python:3.10.5-slim-buster

WORKDIR /api

# prevent python writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# prevent python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --upgrade pip

COPY ./requirements.txt /api/requirements.txt
RUN pip install -r requirements.txt
RUN mkdir -p /root/.deepface/weights

# copy project
COPY . /api/
