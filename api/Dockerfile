FROM python:3.8-slim-buster@sha256:2ce8031b678a8de21815a760313707f145f69ffc80f8d411b2d5f198f47608bf

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /api

COPY ./requirements.txt .

RUN pip install -U pip && \
    pip install -r requirements.txt

COPY . .
