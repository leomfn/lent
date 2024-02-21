#!/bin/sh
if [ "$DEBUG" = 'OFF' ]; then
    echo "Collecting static files"
    python manage.py collectstatic --no-input
    echo "Starting Django application in production environment using gunicorn"
    gunicorn config.wsgi --bind 0.0.0.0:8000
else
    echo "Starting Django application in development environment using manage.py runserver"
    python manage.py runserver 0.0.0.0:8000
fi
