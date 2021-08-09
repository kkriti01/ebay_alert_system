#!/bin/sh

set -o errexit
# shellcheck disable=SC2039
set -o nounset
set -o xtrace
set -o errexit

# shellcheck disable=SC2124
cmd="$@"

export REDIS_URL=redis://redis:6379
export REDIS_HOST=redis

if [ -z "$POSTGRES_USER" ]; then
    export POSTGRES_USER=postgres
fi
export DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@postgres:5432/$POSTGRES_USER
export CELERY_BROKER_URL=$REDIS_URL/0

postgres_ready() {
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="$POSTGRES_USER", user="$POSTGRES_USER", password="$POSTGRES_PASSWORD", host="postgres")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}


until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing..."
exec "$cmd"
