# deploy moviestore Django application
FROM python:3.9-alpine
LABEL maintainer="SokratisTzifkas"

ENV PYTHONBUFFERED=1

COPY ./requirements.txt /requirements.txt
COPY ./moviestore /moviestore

WORKDIR /moviestore
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base \
        postgresql-dev \
        musl-dev \
        && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home --gecos "" moviestore

ENV PATH="/py/bin:$PATH"

USER moviestore