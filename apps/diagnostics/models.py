from django.db import models
from django.conf import settings

class MedicalRecord(models.Model):
    # Links to your Custom User model
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='medical_records'
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='assigned_diagnostics'
    )
    
    # The actual file (X-ray, MRI, Report)
    document = models.FileField(upload_to='medical_records/%Y/%m/%d/')
    
    # Metadata
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_analyzed = models.BooleanField(default=False) # For Week 3 AI integration

    def __str__(self):
        return f"Record: {self.patient.username} - {self.uploaded_at.strftime('%Y-%m-%d')}"