# Create required directories
mkdir -p media staticfiles
touch media/.gitkeep staticfiles/.gitkeep

# Set permissions
chmod -R 755 media staticfiles

# Stop any running containers
docker compose down

# Rebuild and start containers
docker compose up -d --build

# Run migrations
docker compose exec web python manage.py migrate

# Collect static files
docker compose exec web python manage.py collectstatic --noinput