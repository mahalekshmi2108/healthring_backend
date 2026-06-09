from django.contrib import admin
from .models import UserProfile, HealthData, EmergencyAlert, Doctor

admin.site.register(UserProfile)
admin.site.register(HealthData)
admin.site.register(EmergencyAlert)
admin.site.register(Doctor)