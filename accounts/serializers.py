from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from .models import User, UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    mobile = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'mobile')

    @transaction.atomic
    def create(self, validated_data):
        mobile = validated_data.pop('mobile', None)
        user = User.objects.create_user(**validated_data)

        # Update profile (already created by signal)
        if mobile:
            if not mobile.isdigit() or len(mobile) != 10:
                raise serializers.ValidationError("Invalid mobile number")
            else:
                user.profile.mobile = mobile
                user.profile.save()

        return user

class LoginSerializer(TokenObtainPairSerializer):

    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid email or password")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid email or password")

        if not user.is_active:
            raise AuthenticationFailed("Account is inactive")

        data = super().validate(attrs)

        # Add extra response data (optional)
        data["user"] = {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
        }

        return data

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.validated_data['refresh'])
            token.blacklist()
        except Exception:
            self.fail('bad_token')