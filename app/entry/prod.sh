#!/bin/sh

/code/manage.py migrate
/code/manage.py collectstatic --no-input
gunicorn --workers 3 --bind 0.0.0.0:8000 app.wsgi:application