# Base Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (required for OpenCV, PostgreSQL, PyTorch/pydicom)
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    libgl1 \
    libglib2.0-0 \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Create staticfiles directory for WhiteNoise
RUN mkdir -p /app/staticfiles

# Expose port
EXPOSE 8000

# Run gunicorn with 1 worker (Render free tier: 512MB RAM limit)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1", "--timeout", "120"]
