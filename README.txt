username = rizwan
password = 1234

Ready-to-run Django e-commerce PoC (minimal)

Steps to run:

1. Create and activate virtualenv:
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   source .venv/bin/activate  # macOS / Linux

2. Install requirements:
   pip install -r requirements.txt

3. Make migrations and load fixture:
   python manage.py makemigrations
   python manage.py migrate
   python manage.py loaddata fixtures/products.json

4. Create a superuser (optional):
   python manage.py createsuperuser

5. Run server:
   python manage.py runserver

Access the site at http://127.0.0.1:8000/
Admin at http://127.0.0.1:8000/admin/

Notes:
- This project is for local development and PoC only.
- DEBUG=True and a simple SECRET_KEY are used for convenience.
