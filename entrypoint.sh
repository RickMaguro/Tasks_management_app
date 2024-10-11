#!/bin/bash

# Ensure all superuser environment variables are set
if [ -z "$DJANGO_SUPERUSER_USERNAME" ] || [ -z "$DJANGO_SUPERUSER_EMAIL" ] || [ -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Superuser credentials are not fully set."
    exit 1
fi

python manage.py migrate

# Check if a superuser exists, and if not, create one
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
username='$DJANGO_SUPERUSER_USERNAME';
email='$DJANGO_SUPERUSER_EMAIL';
password='$DJANGO_SUPERUSER_PASSWORD';
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password);
    print('Superuser created.');
else:
    print('Superuser already exists.');
"

# Start the server
exec "$@"