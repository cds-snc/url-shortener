FROM python:3.8-slim-buster@sha256:522aebe4ed27435314509f704beda532bc85ec58ecfeefe5225920a89f4cabab

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /api

COPY ./requirements.txt .

RUN pip install -U pip && \
    pip install -r requirements.txt

COPY . .
