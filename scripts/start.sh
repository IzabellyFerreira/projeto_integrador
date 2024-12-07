# scripts/start.sh
#!/bin/bash
set -e

# Wait for database
until nc -z db 5432; do
    echo "Waiting for database..."
    sleep 1
done

# Apply migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start development server
if [ "$DJANGO_DEBUG" = "1" ]; then
    python manage.py runserver 0.0.0.0:8000
else
    gunicorn config.wsgi:application --bind 0.0.0.0:8000
fi