#!/bin/sh

gunicorn -c /usr/src/backend/app/conf/gunicorn_config.py 'app:run()' --reload