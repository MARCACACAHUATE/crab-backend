from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import DatasetSerializer, CreateDatasetSerializer
from .models import Dataset

class DatasetViewSet(viewsets.GenericViewSet):
    queryset = Dataset.objects.all()
    serializer_class = CreateDatasetSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            permissions = [IsAuthenticated]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        data["owner"] = request.user.username
        return Response(data, status=status.HTTP_201_CREATED)
