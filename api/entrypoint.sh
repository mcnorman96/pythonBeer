#!/bin/sh

# Wait for MySQL to be ready
echo "Waiting for MySQL..."

while ! nc -z $MYSQL_HOST 3306; do
  sleep 0.1
done

echo "MySQL started"

# Run migrations
flask db upgrade

# Optionally run seed script here (if you have a separate one)
# python seed.py

exec "$@"
