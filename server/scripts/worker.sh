#!/bin/sh

set -o errexit
set -o nounset
set -o xtrace

celery -A taskapp worker -l INFO
