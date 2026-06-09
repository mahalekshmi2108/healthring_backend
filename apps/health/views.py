from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from .models import UserProfile, HealthData, EmergencyAlert
from .serializers import (
    UserProfileSerializer,
    HealthDataSerializer,
    EmergencyAlertSerializer
)

from apps.accounts.models import UserRole


# ================= PROFILE =================
@api_view(['GET', 'POST'])
def profile_list(request):

    if request.method == 'GET':
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    serializer = UserProfileSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)


# ================= HEALTH DATA =================
@api_view(['GET', 'POST'])
def health_data_list(request):

    if request.method == 'GET':
        data = HealthData.objects.all().order_by('-created_at')
        serializer = HealthDataSerializer(data, many=True)
        return Response(serializer.data)

    serializer = HealthDataSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)


# ================= DASHBOARD =================
@api_view(['GET'])
def dashboard(request):

    latest = HealthData.objects.order_by('-created_at').first()

    if not latest:
        return Response({"message": "No health data found"})

    return Response({
        "heart_rate": latest.heart_rate,
        "spo2": latest.spo2,
        "stress_level": latest.stress_level,
        "sleep_hours": latest.sleep_hours,
        "steps": latest.steps,
        "calories": latest.calories,
    })


# ================= EMERGENCY CHECK =================
@api_view(['GET'])
def emergency_check(request):

    latest = HealthData.objects.order_by('-created_at').first()

    if not latest:
        return Response({"status": "No health data found"})

    alerts = []

    if latest.heart_rate > 120:
        alerts.append("High Heart Rate Detected")

    if latest.spo2 < 90:
        alerts.append("Low Oxygen Level Detected")

    if not alerts:
        return Response({
            "status": "Normal",
            "alerts": []
        })

    return Response({
        "status": "Emergency",
        "alerts": alerts
    })


# ================= EMERGENCY CREATE (FIXED) =================
class EmergencyCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user

        alert = EmergencyAlert.objects.create(
            user=user,
            alert_type="SOS",
            message="Emergency help needed"
        )

        return Response({
            "message": "Emergency alert created",
            "alert_id": alert.id
        })


# ================= DOCTOR DASHBOARD =================
class DoctorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        role = UserRole.objects.get(user=request.user)

        if role.role != "doctor":
            return Response({"error": "Only doctors allowed"})

        patients = UserProfile.objects.filter(
            assigned_doctor__user=request.user
        )

        return Response({
            "doctor": request.user.username,
            "total_patients": patients.count(),
            "patients": [
                {
                    "username": p.user.username,
                    "age": p.age,
                    "gender": p.gender
                }
                for p in patients
            ]
        })


# ================= DOCTOR PATIENTS (by doctor_id) =================
class DoctorPatientsView(APIView):

    def get(self, request, doctor_id):

        patients = UserProfile.objects.filter(
            assigned_doctor_id=doctor_id
        )

        return Response([
            {
                "username": p.user.username,
                "age": p.age,
                "gender": p.gender,
                "height": p.height,
                "weight": p.weight,
            }
            for p in patients
        ])