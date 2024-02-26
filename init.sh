#!/bin/sh
if [ ! -f "${DB_FILE_PATH}/db.sqlite3" ]; then
    echo "No database file was found. This probably means that you have started lent for the first time."
    echo "Creating database"
    python manage.py migrate
    echo "Creating initial superuser with provided credentials"
    DJANGO_SUPERUSER_PASSWORD=${DJANGO_ADMIN_PASSWORD} python manage.py createsuperuser --username "$DJANGO_ADMIN_USERNAME" --email "$DJANGO_ADMIN_EMAIL" --no-input
fi

if [ "$DEBUG" = 'OFF' ]; then
    echo "Collecting static files"
    python manage.py collectstatic --no-input
    echo "Starting Django application in production environment using gunicorn"
    gunicorn config.wsgi --bind 0.0.0.0:8000
else
    echo "Starting Django application in development environment using manage.py runserver"
    python manage.py runserver 0.0.0.0:8000
fi
