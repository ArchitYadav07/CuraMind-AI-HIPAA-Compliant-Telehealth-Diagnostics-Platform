import magic
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

# HIPAA Security: Validator to ensure only medical-grade files are uploaded
def validate_medical_file(file):
    # Read the first 2048 bytes to detect the actual file signature
    file_content = file.read(2048)
    file_mime = magic.from_buffer(file_content, mime=True)
    file.seek(0)  # Reset pointer so Django can save the file later

    # Allowed types for a diagnostic platform
    accepted_types = [
        'image/jpeg', 
        'image/png', 
        'application/dicom',  # Standard Medical Imaging
        'application/pdf'     # Medical Reports
    ]

    if file_mime not in accepted_types:
        raise ValidationError(
            f"Security Alert: Unsupported file type ({file_mime}). "
            "Only X-rays (JPEG/PNG), MRIs (DICOM), or PDFs are allowed."
        )

class MedicalRecord(models.Model):
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
    
    # Document field now includes the security validator
    document = models.FileField(
        upload_to='medical_records/%Y/%m/%d/',
        validators=[validate_medical_file]
    )
    
    # Store the generated AI heatmap
    heatmap_image = models.ImageField(
        upload_to='medical_records/heatmaps/%Y/%m/%d/',
        blank=True,
        null=True
    )
    
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_analyzed = models.BooleanField(default=False)

    def __str__(self):
        return f"Record: {self.patient.username} - {self.uploaded_at.strftime('%Y-%m-%d')}"
    
@receiver(post_save, sender=MedicalRecord)
def trigger_ai_analysis(sender, instance, created, **kwargs):
    if created:
        from celery import current_app
        current_app.send_task(
            'apps.diagnostics.tasks.process_medical_image', # Add the 's' here!
            args=[instance.id]
        )