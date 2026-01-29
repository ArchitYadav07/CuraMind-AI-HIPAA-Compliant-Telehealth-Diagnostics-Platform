from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import MedicalRecord

@login_required
def patient_dashboard(request):
    # This ensures Patient A cannot see Patient B's X-rays
    my_reports = MedicalRecord.objects.filter(patient=request.user).order_by('-uploaded_at')
    return render(request, 'diagnostics/patient_dashboard.html', {'reports': my_reports})