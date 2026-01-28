from django.contrib import admin
from .models import MedicalRecord

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'uploaded_at', 'is_analyzed')
    list_filter = ('is_analyzed', 'uploaded_at')
    search_fields = ('patient__username', 'description')