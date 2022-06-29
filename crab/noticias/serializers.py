from rest_framework import serializers

from .models import Noticia, Categoria, Pagina

class NoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = "__all__"


class CreateNoticiaSerializer(serializers.Serializer):
    titulo = serializers.CharField(max_length = 40)
    contenido = serializers.CharField(max_length = 255)
    fecha = serializers.DateTimeField()
    categoria = serializers.CharField(max_length=40)
    pagina = serializers.CharField(max_length=40)
    

    def validate_categoria(self, data):
        """Verifica que la categoria exista, sino la crea. """
        obj, cereated = Categoria.objects.get_or_create(categoria=data)
        self.context['categoria'] = obj
        return data

    def validate_pagina(self, data):
        try:
            self.context['pagina'] = Pagina.objects.get(nombre_pagina=data)
        except Pagina.DoesNotExist:
            raise serializers.ValidationError("La pagina no existe")
        return data

    def create(self, data):
        categoria = self.context['categoria']
        pagina = self.context['pagina']

        pirinola = {
            "titulo": data["titulo"],
            "contenido": data["contenido"],
            "fecha": data["fecha"],
        }
        noticia = Noticia.objects.create(**pirinola, categoria=categoria, pagina=pagina)

        print(noticia)
        return noticia
    
