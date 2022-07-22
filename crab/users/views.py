from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from .models import User
from .permissions import IsAccountOwner
from .serializers import (
        StatusSerializer,
        UserSerializer,
        UserUpdateSerializer,
        UserLoginSerializer,
        UserSignUpSerializer,
        AccountVerificationSerializer
        )


class UserViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet
        ):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ["update","partial_update"]:
            return UserUpdateSerializer
        if self.action == "login":
            return UserLoginSerializer
        if self.action == "create":
            return UserSignUpSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ["update","partial_update"]:
            permissions = [IsAccountOwner, IsAuthenticated]
        elif self.action in ["create", "login", "verify"]:
            permissions = [AllowAny]
        elif self.action in ["list", "status"]:
            permissions = [IsAdminUser, IsAuthenticated]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    @action(detail=True, methods=["post"], serializer_class=StatusSerializer)
    def status(self, request, pk = None):
        
        if "is_active" not in request.data.keys():
            return Response({"required": "is_active is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = self.get_object()
        serializer = UserSerializer(user, data={"is_active": request.data["is_active"]}, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                "username": serializer.data["username"],
                "is_active": serializer.data["is_active"],
            }
            return Response(data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data)

    @action(detail=False, methods=["post"])
    def verify(self, request):
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Cuenta verificada"}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)
