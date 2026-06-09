from django.urls import path
from .views import (
    profile_list,
    health_data_list,
    dashboard,
    emergency_check,
    DoctorPatientsView,
    DoctorDashboardView,
    EmergencyCreateView
)

urlpatterns = [
    path('profiles/', profile_list),
    path('health-data/', health_data_list),
    path('dashboard/', dashboard),
    path('emergency-check/', emergency_check),

    path("doctor/<int:doctor_id>/patients/", DoctorPatientsView.as_view()),

    path("doctor/dashboard/", DoctorDashboardView.as_view()),

    path("emergency/create/", EmergencyCreateView.as_view()),
]