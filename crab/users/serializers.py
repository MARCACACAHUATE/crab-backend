from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, password_validation

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
        print(data)
        user = User.objects.create_user(**data) 
        return user

