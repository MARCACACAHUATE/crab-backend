from datetime import timedelta

import jwt
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, password_validation
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from crab import settings
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, min_length=1, required=True)
    password = serializers.CharField(max_length=50, min_length=1, required=True)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        tokens = {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
            }
        return tokens

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Credenciales Invalidas")
        if not user.is_verified:
            raise serializers.ValidationError("Usuario no verificado")
        self.context["user"] = user
        return data

    def create(self, validated_data):
        tokens = self.get_token_for_user(self.context["user"])
        return tokens


class StatusSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=True)


class UserSignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, min_length=1, required=True)
    password = serializers.CharField(min_length=4)
    password_confirm = serializers.CharField(min_length=4)
    email = serializers.EmailField()

    def validate(self, validate_data):
        if validate_data["password"] != validate_data["password_confirm"]:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        password_validation.validate_password(validate_data["password"])
        return validate_data

    def create(self, data):
        data.pop("password_confirm")
        user = User.objects.create_user(**data) 
        self.send_email_confirmation(user)
        return user

    def send_email_confirmation(self, user):
        token = self.gen_verification_token(user)
        subject = "tu pinche cola"
        from_email = "crab@crab.com"
        content = render_to_string(
                "users/emails/account_verification.html",
                {"token": token, "user": user}
                )
        msg = EmailMultiAlternatives(subject, content, from_email, to=[user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def gen_verification_token(self, user):
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            "user": user.username,
            "exp": int(exp_date.timestamp()),
            "type": "email_confirmation",
            }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token


class AccountVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate_token(self, data):
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Verification link has expired")
        except jwt.PyJWTError:
            raise serializers.ValidationError("Invalid token")

        if payload["type"] != "email_confirmation":
            raise serializers.ValidationError("Invalid token")

        self.context["payload"] = payload
        return data

    def save(self, **kwargs):
        payload = self.context["payload"]
        user = User.objects.get(username=payload["user"])
        user.is_verified = True
        user.save()
        
