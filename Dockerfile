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
# Ensure missing production dependencies are present
RUN pip install gunicorn psycopg2-binary django-storages boto3 pydicom

# Copy project
COPY . /app/

# Expose port
EXPOSE 8000

# Run gunicorn (this command is generally overridden by docker-compose for workers)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
