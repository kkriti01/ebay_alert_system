#!/bin/sh

set -o errexit
set -o nounset
set -o xtrace

# for production
#daphne -b 0.0.0.0 -p 8000 shore.asgi:application


# only for dev deployments
python manage.py collectstatic --noinput
python manage.py runserver "0.0.0.0:8000"
