#!/bin/sh
set -e

echo "-- Waiting for database..."
# HACK: not sure how to wait for mysql to be ready
sleep 3

echo "-- Running migrations..."
python manage.py migrate --noinput

echo "-- Starting"
python manage.py runserver 0.0.0.0:${PORT:-8000}