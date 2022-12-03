#!/bin/sh

set -e

# activate our virtual environment here
. "$VENV_PATH"/bin/activate

cd src && ./manage.py migrate && ./manage.py collectstatic -i "admin/*" -i "baton/*"

gunicorn --reload --chdir /app/src -b :8000 --access-logfile - app.wsgi:application
