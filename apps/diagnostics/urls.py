from django.urls import path
from .views import patient_dashboard, admin_dashboard

urlpatterns = [
    # This URL will be: http://127.0.0.1:8000/diagnostics/my-reports/
    path('my-reports/', patient_dashboard, name='patient_dashboard'),
    # This URL will be: http://127.0.0.1:8000/diagnostics/admin-board/
    path('admin-board/', admin_dashboard, name='admin_dashboard'),
]