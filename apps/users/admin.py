from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# This tells Django how to display your custom fields in the admin
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'is_doctor', 'is_patient', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Roles', {'fields': ('is_doctor', 'is_patient', 'medical_id')}),
    )

admin.site.register(User, CustomUserAdmin)