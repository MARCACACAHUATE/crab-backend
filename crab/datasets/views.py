import csv, io

from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser, JSONParser

from .serializers import DatasetSerializer, CreateDatasetSerializer, ImportDatasetSerializer
from .models import Dataset
from noticias.models import Noticia
from .permissions import IsDatasetOwner


class DatasetViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    parser_classes = [JSONParser, FileUploadParser]

    def get_serializer_class(self):
        if self.action == "list":
            return DatasetSerializer
        return CreateDatasetSerializer

    def get_permissions(self):
        if self.action in ["create", "file", "list"]:
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

    @action(methods=["post"], detail=False)
    def file(self, request):
        serializer = ImportDatasetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data["file"]
        data = {}
        with io.TextIOWrapper(file, encoding="utf-8") as text_file:
            reader = csv.DictReader(text_file)
            total = 0
            for row in reader:
                print("hola")
                total+= 1
                Noticia.objects.create(**row)

            data["noticias_importadas"] = total
        return Response(data)
