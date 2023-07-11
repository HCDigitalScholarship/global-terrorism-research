#!/bin/sh
set -e

echo "-- Waiting for database..."
sleep 3

# echo "-- Running migrations..."
# python manage.py migrate --noinput

echo "-- Starting"
python manage.py runserver 0.0.0.0:8000