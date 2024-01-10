#!/bin/bash
# # Define source and destination paths for media folder
# media_source="/media"
# media_destination="/app/media"
# # Copy the media folder
# cp -r "$media_source" "$media_destination"
# daphne chat.asgi:application --port $PORT --bind 0.0.0.0 -v2
# celery -A ecom.celery worker -l info --concurrency 1


#!/bin/bash
cp -r media /app
# python manage.py clearcache
python manage.py migrate && python manage.py collectstatic --noinput
daphne chat.asgi:application --port $PORT --bind 0.0.0.0 -v2
# hypercorn --bind 0.0.0.0:$PORT personal_portfolio.asgi:application

# Define source and destination paths for media folder
# media_source="media"
# media_destination="/app/media"
# # Copy the media folder
# cp -r "$media_source" "$media_destination"
# Create a directory for the media files
# mkdir -p /app/media
# # Copy the media folder
# cp -r media /app
# cd media
# ls