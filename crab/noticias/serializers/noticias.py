from rest_framework import serializers

from noticias.models import Noticia, Categoria, Pagina


class NoticiaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = "__all__"


class CreateNoticiaSerializer(serializers.Serializer):
    titulo = serializers.CharField(max_length = 40)
    contenido = serializers.CharField(max_length = 255)
    fecha = serializers.DateTimeField()
    categoria = serializers.CharField(max_length=40)

    def validate_categoria(self, data):
        """Verifica que la categoria exista, sino la crea. """
        obj, cereated = Categoria.objects.get_or_create(categoria=data)
        self.context['categorias'].append(obj)
        return data


class ListNoticiaSerializer(serializers.Serializer):
    pagina = serializers.CharField(max_length=38)
    noticias = CreateNoticiaSerializer(many=True)

    def validate_pagina(self, data):
        try:
            self.context['pagina'] = Pagina.objects.get(nombre_pagina=data)
        except Pagina.DoesNotExist:
            raise serializers.ValidationError("La pagina no existe")
        return data

    def create(self, data):
        pagina = self.context['pagina']
        categorias = self.context["categorias"]
        noticias = data["noticias"]
        data = {
                "pagina": pagina,
                "noticias": []
            }

        for key, noticia in enumerate(noticias):
            noticia.pop("categoria")
            data["noticias"].append(Noticia.objects.create(**noticia, categoria=categorias[key], pagina=pagina))


        print(data)

        return data



