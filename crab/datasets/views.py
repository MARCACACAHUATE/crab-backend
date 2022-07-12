from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import CreateDatasetSerializer
from .models import Dataset
from .permissions import IsDatasetOwner

class DatasetViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Dataset.objects.all()
    serializer_class = CreateDatasetSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            permissions = [IsAuthenticated]
        elif self.action in ["destroy"]:
            permissions = [IsDatasetOwner, IsAuthenticated]
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
