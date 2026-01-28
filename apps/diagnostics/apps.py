from django.apps import AppConfig


# apps/diagnostics/apps.py

class DiagnosticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.diagnostics'  # Add the 'apps.' prefix here