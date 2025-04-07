from rest_framework import serializers
from .models import CustomUser as User, Invoice, Wallet, VirtualCard
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
import pyotp
from io import BytesIO
import qrcode
from django.contrib.auth import authenticate



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'two_factor_enabled']
        extra_kwargs = {
                    "password": {"write_only": True},
                    "qr_code": {"read_only": True},
                }

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class LogoutSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()

class TwoFASerializer(serializers.Serializer):
    user_id = serializers.UUIDField()

class OTPVerifySerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    code = serializers.CharField(max_length=6)
