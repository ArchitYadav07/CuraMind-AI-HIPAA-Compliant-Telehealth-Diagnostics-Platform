# apps/appointments/admin.py
from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'scheduled_time', 'status')
    list_filter = ('status', 'scheduled_time')
    search_fields = ('patient__username', 'doctor__username')

    # Custom logic to filter the dropdowns in the Admin interface
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor":
            # Only show users where is_doctor is True
            kwargs["queryset"] = db_field.related_model.objects.filter(is_doctor=True)
        if db_field.name == "patient":
            # Only show users where is_patient is True
            kwargs["queryset"] = db_field.related_model.objects.filter(is_patient=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)