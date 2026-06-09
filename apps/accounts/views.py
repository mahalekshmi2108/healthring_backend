from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserRole
from apps.health.models import UserProfile   # NEW IMPORT


# ================= REGISTER =================
@api_view(['POST'])
def register(request):

    username = request.data.get('username')
    password = request.data.get('password')
    role = request.data.get('role', 'user')

    if not username or not password:
        return Response({"error": "Username and password required"})

    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"})

    # Create User
    user = User.objects.create_user(
        username=username,
        password=password
    )

    # Assign Role
    UserRole.objects.create(
        user=user,
        role=role
    )

    # Create Empty Profile
    UserProfile.objects.create(
        user=user
    )

    return Response({
        "message": "User created successfully",
        "username": user.username,
        "role": role
    })


# ================= LOGIN (JWT) =================
@api_view(['POST'])
def login(request):

    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(
        username=username,
        password=password
    )

    if user is None:
        return Response({
            "error": "Invalid credentials"
        })

    refresh = RefreshToken.for_user(user)

    return Response({
        "user_id": user.id,
        "username": user.username,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    })