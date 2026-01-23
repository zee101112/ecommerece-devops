#!/usr/bin/env bash
set -e

python manage.py migrate --noinput

python - <<'PY'
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")
django.setup()
from shop.models import Product
from django.core.management import call_command

# Load default products if DB is empty
if Product.objects.count() == 0:
    call_command("loaddata", "shop/fixtures/products.json")
    print("Loaded default products from fixture.")
else:
    print("Products already exist; not reloading fixture.")
PY

python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000
