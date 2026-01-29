from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import MedicalRecord

@login_required
def patient_dashboard(request):
    # Security: Filter records strictly by the logged-in user
    reports = MedicalRecord.objects.filter(patient=request.user).order_by('-uploaded_at')
    return render(request, 'diagnostics/patient_dashboard.html', {'reports': reports})