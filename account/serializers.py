from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.models import Account


UserModel = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = Account.USERNAME_FIELD


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'first_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate_phone(self, value):
        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError('Phone number must be 10 digits')
        if UserModel.objects.filter(phone=value).exists():
            raise serializers.ValidationError('Phone already exists')
        return value

    def validate_password(self, value):
        validate_password(value)
        return value


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
