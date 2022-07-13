from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import DatasetSerializer, CreateDatasetSerializer
from .models import Dataset
from .permissions import IsDatasetOwner

class DatasetViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):

    def get_serializer_class(self):
        if self.action == "list":
            return DatasetSerializer
        return CreateDatasetSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            permissions = [IsAuthenticated]
        elif self.action in ["destroy", "update", "partial_update"]:
            permissions = [IsDatasetOwner, IsAuthenticated]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]

    def get_queryset(self):
        owner = self.request.user
        queryset = Dataset.objects.filter(user=owner)
        return queryset

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        data["owner"] = request.user.username
        return Response(data, status=status.HTTP_201_CREATED)
