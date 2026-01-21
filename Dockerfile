# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Expose port (Render provides $PORT, but exposing is fine)
EXPOSE 8000

# Run migrations + collectstatic + start server
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    python manage.py shell < createsuperuser.py && \
    gunicorn ecommerce_project.wsgi:application --bind 0.0.0.0:${PORT:-8000}
