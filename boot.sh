#!/bin/bash
# this script is used to boot a Docker container with Daphne

# Wait for the database to be ready if necessary
while true; do
    python manage.py migrate --noinput
    if [ "$?" -eq 0 ]; then
        break
    fi
    echo "Migration command failed, retrying in 5 secs..."
    sleep 5
done

# Collect static files
python manage.py collectstatic --noinput

# После выполнения миграций и сбора статических файлов, запускаем Daphne
exec daphne -b 0.0.0.0 -p 8000 django_luda_project.routing:application