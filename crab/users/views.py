from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import User
from .serializers import StatusSerializer, UserSerializer, UserUpdateSerializer, UserLoginSerializer
from .permissions import IsAccountOwner


class UserViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet
        ):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action in ["update","partial_update"]:
            return UserUpdateSerializer
        if self.action == "login":
            return UserLoginSerializer
        return UserSerializer

    def get_permissions(self):
        permissions = []
        if self.action in ["update","partial_update"]:
            permissions.append(IsAccountOwner)
            permissions.append(IsAdminUser)
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
