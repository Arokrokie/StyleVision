#!/bin/bash

# Exit on error
set -e

echo "Starting Django deployment..."

# Run database migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files (if not done in build)
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    hair_project.wsgi:application
