FROM python:3.8-slim-buster

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /api

COPY ./requirements.txt .

RUN pip install -U pip && \
    pip install -r requirements.txt

COPY . .
