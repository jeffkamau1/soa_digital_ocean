from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import render

from accounts.api.serializers import (UserRegistrationSerializer, UserSerializer,
                                      LoginSerializer, RoleSerializer)
from accounts.api.permissions import IsTeamLead
from accounts.models import CustomUser, Role
from drf_spectacular.utils import extend_schema
from utils.send_email_verification import send_verification_email


@extend_schema(
    request=UserRegistrationSerializer,
    responses=None
)
@api_view(['POST', ])
def register_user_view(request):
    """
    This is the endpoint to register a new user
    """
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_email = send_verification_email(user)
            print(response_email)
            return Response({'message': 'Hurayyy! You have been registered successfully!',
                             'user': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses=None
)
@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, token):
    try:
        user = CustomUser.objects.get(email_verification_token=token)
        user.is_email_verified = True
        user.email_verification_token = None
        user.save()
        return Response({'message': 'Email verification successful'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'Invalid verification token'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(request=LoginSerializer, responses=None)
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUsers(generics.ListAPIView):
    """This end point lists all users"""
    serializer_class = UserSerializer

    @extend_schema(request=UserSerializer, responses=None)
    def get_queryset(self):
        queryset = CustomUser.objects.all()
        return queryset


class RetrieveUsers(generics.RetrieveAPIView):
    """This endpoint retrieves an individual user"""
    serializer_class = UserSerializer

    @extend_schema(request=UserSerializer, responses=None)
    def get_queryset(self):
        queryset = CustomUser.objects.all()
        return queryset


class ListRoles(generics.ListAPIView):
    """This endpoint lists all roles eg problem management, Incident Manager"""
    serializer_class = RoleSerializer

    @extend_schema(request=RoleSerializer, responses=None)
    def get_queryset(self):
        queryset = Role.objects.all()
        return queryset


class RetrieveRoles(generics.RetrieveAPIView):
    """THis endpoint retrieves a single role"""
    serializer_class = RoleSerializer

    @extend_schema(request=RoleSerializer, responses=None)
    def get_queryset(self):
        queryset = Role.objects.all()
        return queryset


class NonVerifiedUsersListView(generics.ListAPIView):
    """This endpoint lists all non verified users to team lead"""
    serializer_class = UserSerializer
    permission_classes = [IsTeamLead]

    @extend_schema(request=UserSerializer, responses=None)
    def get_queryset(self):
        user_role = self.request.user.role
        queryset = CustomUser.objects.filter(role=user_role, is_verified=False)
        return queryset


class NonVerifiedUsersRetrieveView(generics.RetrieveAPIView):
    """This endpoint retrieves a single non verified user"""
    serializer_class = UserSerializer
    permission_classes = [IsTeamLead]

    @extend_schema(request=UserSerializer, responses=None)
    def get_queryset(self):
        user_role = self.request.user.role
        queryset = CustomUser.objects.filter(role=user_role, is_verified=False)
        return queryset


class VerifyUserView(generics.UpdateAPIView):
    """Allows team lead to verify user, we just edit is_verified to true"""
    serializer_class = UserSerializer
    permission_classes = [IsTeamLead]
    allowed_methods = ['PATCH']

    @extend_schema(request=UserSerializer, responses=None)
    def get_queryset(self):
        user_role = self.request.user.role
        queryset = CustomUser.objects.filter(role=user_role, is_verified=False)
        return queryset

    def perform_update(self, serializer):
        serializer.instance.is_verified = True
        serializer.instance.save()


def email_template(request):
    return render(request, 'email_verification.html')
