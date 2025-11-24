#!/bin/bash
set -e

# Start redis-server in background
service redis-server start

# Start MariaDB service in the background
service mariadb start

# Activate virtual environment
source /usr/local/app/site/venv/bin/activate

# Run Django management commands
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compilemessages
python manage.py compilejsi18n

# Start supervisor to manage uwsgi and nginx
exec supervisord -n
