# Use the official Python 3 image.
# https://hub.docker.com/_/python
#
# python:3 builds a 954 MB image - 342.3 MB in Google Container Registry
# FROM python:3
#
# python:3-slim builds a 162 MB image - 51.6 MB in Google Container Registry
# FROM python:3-slim
#
# python:3-alpine builds a 97 MB image - 33.2 MB in Google Container Registry
FROM python:3.8-slim

# Create and change to the app directory.
COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# This default value facilitates local development.
ENV PORT 8080
ENV PREDICT_REST_API_URL "https://handwritten-sudoku-ocahlgdqhq-uc.a.run.app/predict"

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 main:app