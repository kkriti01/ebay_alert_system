#!/bin/sh

set -o errexit
set -o nounset
set -o xtrace



rm -f './celerybeat*'
celery -A taskapp beat -l INFO
