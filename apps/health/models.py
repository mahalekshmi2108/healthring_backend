from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)

    assigned_doctor = models.ForeignKey(
        "Doctor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username

    def __str__(self):
        return self.user.username

class HealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    heart_rate = models.IntegerField()
    spo2 = models.FloatField()
    stress_level = models.IntegerField()

    sleep_hours = models.FloatField()
    steps = models.IntegerField()
    calories = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
    #===========emergency alert====================== 
class EmergencyAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    alert_type = models.CharField(max_length=100)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.alert_type}"
# ===============Doctor module=================

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name