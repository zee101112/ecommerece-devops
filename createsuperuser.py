import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if username and password:
    user, created = User.objects.get_or_create(username=username, defaults={"email": email or ""})
    if created or not user.is_staff or not user.is_superuser:
        user.email = email or user.email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        print("Superuser ensured/updated.")
    else:
        print("Superuser already OK.")
else:
    print("Superuser env vars not set.")
