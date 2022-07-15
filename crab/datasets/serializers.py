from datetime import datetime
from zoneinfo import ZoneInfo

from rest_framework import serializers
from .models import Dataset
from noticias.models import Noticia


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = "__all__"


class CreateDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ["fecha_inicio", "fecha_final"]

    def validate_fecha_inicio(self, data):
        primera_noticia = Noticia.objects.order_by("fecha")[0].fecha
        fecha_inicio = datetime.combine(data, datetime.min.time()).astimezone(tz=ZoneInfo("America/Mexico_City"))
        if fecha_inicio < primera_noticia:
            raise serializers.ValidationError(f"No hay noticias antes de esta fecha: primera noticia registarda => {primera_noticia}")
        return data

    def validate_fecha_final(self, data):
        ultima_noticia = Noticia.objects.order_by("-fecha")[0].fecha
        fecha_final = datetime.combine(data, datetime.min.time()).astimezone(tz=ZoneInfo("America/Mexico_City"))
        if fecha_final > ultima_noticia:
            raise serializers.ValidationError(f"No hay noticias despues de esta fecha: ultima noticia registrada => {ultima_noticia}")
        return data

    def create(self, data):
        data = {
            "fecha_inicio": data["fecha_inicio"],
            "fecha_final": data["fecha_final"],
            "user": self.context["request"].user
            }
        dataset = Dataset.objects.create(**data)

        return dataset


class ImportDatasetSerializer(serializers.Serializer):
    file = serializers.FileField()
