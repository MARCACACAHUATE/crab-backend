from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .serializers import StatusSerializer, UserSerializer


class UserViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
