#!/bin/sh

set -o errexit
set -o nounset
set -o xtrace

python manage.py migrate
daphne -b 0.0.0.0 -p 8000 shore.asgi:application
