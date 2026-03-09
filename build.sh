#!/usr/bin/env bash
# build.sh — Render runs this script during every deployment

set -o errexit  # Exit on any error

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files (WhiteNoise will serve them)
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate
