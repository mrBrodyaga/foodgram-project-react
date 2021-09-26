#!/usr/bin/env sh

set -o errexit
set -o nounset

python /code/manage.py makemigrations api
python /code/manage.py makemigrations users
python /code/manage.py migrate --noinput
python /code/manage.py collectstatic --noinput

gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
