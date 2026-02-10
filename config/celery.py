import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('CuraMindAI')
app.config_from_object('django.conf:settings', namespace='CELERY')

# This tells Celery: "Look inside the 'apps' folder for any 'tasks.py' files"
app.autodiscover_tasks(['apps.diagnostics'])