import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if not username or not password:
    print("Missing DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD")
    raise SystemExit(0)

user, created = User.objects.get_or_create(username=username, defaults={"email": email})

# Always ensure it is staff + superuser and password matches env var
user.email = email or user.email
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()

print("Superuser ensured:", username, "(created)" if created else "(updated)")
