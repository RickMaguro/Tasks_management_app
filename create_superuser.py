import os 
import django

from django.contrib.auth.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wellence_project.settings")
django.setup()

def create_superuser():
    username = os.getenv("SUPER_USERNAME")
    email = os.getenv("SUPERUSER_EMAIL")
    password = os.getenv("SUPERUSER_PASSWORD")

    if User.objects.filter(username=username).exists():
        print("Superuser already exists")
    else: 
        User.objects.create_superuser(username=username, password=password, email=email)
        print("Superuser successfully created")

if __name__ == "__main__":
    create_superuser()