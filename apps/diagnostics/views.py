from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import MedicalRecord

@login_required
def patient_dashboard(request):
    # Security: Ensure only patients can access this view
    if not request.user.is_patient:
        return HttpResponseForbidden("You do not have permission to view the Patient Dashboard.")
        
    # Security: Filter records strictly by the logged-in user
    reports = MedicalRecord.objects.filter(patient=request.user).order_by('-uploaded_at')
    
    # We use .htm based on the current disk state (patient_dashboard.htm)
    return render(request, 'diagnostics/patient_dashboard.htm', {'reports': reports})

@login_required
def admin_dashboard(request):
    # Security: Ensure only doctors or superusers can access this view
    if not (request.user.is_doctor or request.user.is_superuser):
        return HttpResponseForbidden("You do not have permission to view the Admin/Doctor Dashboard.")
        
    # Superusers see everything. Doctors see only their assigned records.
    if request.user.is_superuser:
        reports = MedicalRecord.objects.all().order_by('-uploaded_at')
    else:
        reports = MedicalRecord.objects.filter(doctor=request.user).order_by('-uploaded_at')
        
    return render(request, 'diagnostics/admin_dashboard.htm', {'reports': reports})