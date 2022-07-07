from rest_framework import serializers

from noticias.models import Categoria


class CategoriaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"

    def validate(self, data):
        """Verifica que la categoria exista, sino la crea. """
        obj, cereated = Categoria.objects.get_or_create(categoria=data)
        self.context['categoria'] = obj
        return data
