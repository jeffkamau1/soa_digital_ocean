import secrets

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accounts.models import CustomUser, Role
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from utils.send_email_verification import send_verification_email


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    # to validate that email and username don't already exist
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all(), message="This email already exists")]
    )

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'password',
            'confirm_password',
            'is_team_lead',
            'is_verified',
            'is_email_verified',
            'role',
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
        }

    # we are overriding the validate class provided by DRF
    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("The passwords do not match.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        user = CustomUser(
            **validated_data
        )
        user.set_password(password)
        user.email_verification_token = secrets.token_urlsafe(20)
        user.save()
        return user
        # "alternative"
        # validated_data.pop('confirm_password', None)
        # return super().create(validated_data)
        # validated_data.pop('confirm_password', None)
        # user = super().create(validated_data)
        # user.email_verification_token = secrets.token_urlsafe(20)
        # user.save()
        # return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'is_team_lead',
            'is_email_verified',
            'is_verified',
            'role',

        ]


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')

        refresh = RefreshToken.for_user(user)

        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }
