#!/usr/bin/env bash
set -e

echo "Running migrations..."
python manage.py migrate

echo "Loading default products if DB is empty..."
python manage.py shell -c "
from shop.models import Product
from django.core.management import call_command

if Product.objects.count() == 0:
    call_command('loaddata', 'shop/fixtures/products.json')
    print('Loaded default products from fixture.')
else:
    print('Products already exist; skipping fixture load.')
"

echo "Ensuring admin superuser..."
python manage.py shell -c "
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get('DJANGO_ADMIN_USERNAME')
email    = os.environ.get('DJANGO_ADMIN_EMAIL', '')
password = os.environ.get('DJANGO_ADMIN_PASSWORD')

if not username or not password:
    print('⚠️ Admin env vars not set; skipping superuser creation.')
else:
    u, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email}
    )
    u.is_staff = True
    u.is_superuser = True
    u.set_password(password)   # always enforce password
    u.save()
    print(f'✅ Admin ensured: {username} (created={created})')
"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
