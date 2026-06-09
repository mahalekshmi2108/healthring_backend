from rest_framework import serializers
from .models import UserProfile, HealthData, EmergencyAlert
from rest_framework import serializers
from .models import Doctor


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class HealthDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthData
        fields = "__all__"


class EmergencyAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyAlert
        fields = "__all__"

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"