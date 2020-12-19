#!/bin/sh

/code/manage.py migrate
gunicorn --workers 3 --bind 0.0.0.0:8000 app.wsgi:application