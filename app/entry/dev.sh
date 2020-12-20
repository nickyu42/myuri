#!/bin/sh

/code/manage.py migrate
/code/manage.py collectstatic --no-input
/code/manage.py runserver 0.0.0.0:8000