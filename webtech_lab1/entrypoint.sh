#!/bin/bash
set -e

echo "PostgreSQL started"

python manage.py migrate --noinput
python manage.py loaddata data.json

exec "$@"
