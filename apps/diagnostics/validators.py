# apps/diagnostics/validators.py
import magic
from django.core.exceptions import ValidationError

def validate_file_type(file):
    accepted_types = ['image/jpeg', 'image/png', 'application/dicom']
    file_type = magic.from_buffer(file.read(2048), mime=True)
    if file_type not in accepted_types:
        raise ValidationError(f"Unsupported file type: {file_type}. Please upload X-rays or MRIs.")