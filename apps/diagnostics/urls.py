from django.urls import path
from .views import patient_dashboard

urlpatterns = [
    # This URL will be: http://127.0.0.1:8000/diagnostics/my-reports/
    path('my-reports/', patient_dashboard, name='patient_dashboard'),
]