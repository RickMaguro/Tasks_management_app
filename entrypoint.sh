#!/bin/bash

python manage.py migrate

# Check if a superuser exists, and if not, create one
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); \
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists(): \
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD'); \
    print('Superuser created.'); \
else: \
    print('Superuser already exists.');"

# Start the server
exec "$@"