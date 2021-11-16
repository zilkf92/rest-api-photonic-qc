#!/bin/sh
set -e

# Test connection with psql and echo result to console.
until psql $DATABASE_URL -c '\l'; do
    echo >&2 "Postgres is unavailable - sleeping"
    sleep 1
done

echo >&2 "Postgres is up - continuing"

# Make sure media is writable by daphne process.
echo >&2 "correct ownership of media"
chown -Rv 1000:2000 /code/media/

# Migrate database for deployment.
if [ "$1" = "/code/run_asgi.sh" ]; then
    /venv/bin/python manage.py migrate --noinput
fi

# Load Initial Data for deployment.
if [ "x$DJANGO_LOAD_INITIAL_DATA" = 'xon' ]; then
    /venv/bin/python manage.py load_initial_data
fi

exec "$@"



