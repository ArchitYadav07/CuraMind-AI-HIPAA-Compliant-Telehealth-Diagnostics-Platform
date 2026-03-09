"""
Django settings for CuraMind project.
Supports both local development and Render.com production deployment.
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ──────────────────────────────────────────────────────────────────────────────
# SECURITY — read from environment in production, fallback for local dev
# ──────────────────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-n_syhf84hr5qo=fk!^ahfws-q6ogo1ub6j20lrs+25f-1_e()i'  # local dev only
)

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Allow localhost for dev + Render's auto-injected hostname for production
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# ──────────────────────────────────────────────────────────────────────────────
# Application definition
# ──────────────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',  # AWS S3 Storage
    'apps.users',
    'apps.diagnostics',
    'apps.appointments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files on Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ──────────────────────────────────────────────────────────────────────────────
# Database
# In production (Render): DATABASE_URL is auto-set from the linked PostgreSQL.
# In local dev: falls back to your local PostgreSQL credentials.
# ──────────────────────────────────────────────────────────────────────────────
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Production: Render injects this automatically
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    # Local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'CuraMind-AI',
            'USER': 'postgres',
            'PASSWORD': 'Archit0007',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }

# ──────────────────────────────────────────────────────────────────────────────
# Password validation
# ──────────────────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ──────────────────────────────────────────────────────────────────────────────
# Internationalization
# ──────────────────────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ──────────────────────────────────────────────────────────────────────────────
# Static files — WhiteNoise serves them directly on Render (no CDN needed)
# ──────────────────────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ──────────────────────────────────────────────────────────────────────────────
# Media files
# ──────────────────────────────────────────────────────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/diagnostics/my-reports/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ──────────────────────────────────────────────────────────────────────────────
# Celery — optional, only active if REDIS_URL is set (not available on free tier)
# ──────────────────────────────────────────────────────────────────────────────
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# ──────────────────────────────────────────────────────────────────────────────
# AWS S3 Secure Storage (HIPAA Compliance Level)
# ──────────────────────────────────────────────────────────────────────────────
USE_S3 = os.getenv('USE_S3') == 'TRUE'

if USE_S3:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
    AWS_DEFAULT_ACL = 'private'
    AWS_QUERYSTRING_AUTH = True
    AWS_QUERYSTRING_EXPIRE = 300  # Link expires in 5 minutes
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
