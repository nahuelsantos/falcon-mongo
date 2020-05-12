FROM python:3.8.2-alpine3.11

WORKDIR /usr/src/backend/app

COPY requirements.txt  /usr/src/backend

RUN pip install --upgrade pip
RUN pip install -r /usr/src/backend/requirements.txt

COPY ./app  /usr/src/backend/app
COPY docker-entrypoint.sh /usr/src/backend/scripts/docker-entrypoint.sh

RUN chmod +x /usr/src/backend/scripts/docker-entrypoint.sh

ENTRYPOINT ["/usr/src/backend/scripts/docker-entrypoint.sh"]