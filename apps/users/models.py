from django.db import models

# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser): # <--- Ensure this class is named "User"
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    medical_id = models.CharField(max_length=20, blank=True, null=True)