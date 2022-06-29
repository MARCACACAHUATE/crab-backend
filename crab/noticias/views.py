from rest_framework import mixins, viewsets

from .serializers import CreateNoticiaSerializer
from .models import Noticia, Categoria, Pagina

class NoticiaViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Noticia.objects.all()
    serializer_class = CreateNoticiaSerializer
    
    
    #def dispatch(self, request, *args, **kwargs):
    #    self.name_categoria = request.data["name_categoria"]
    #    self.name_pagina = request.data["name_"]
    #    texto = "Arriva las pinches chivas osi osi"
    #    print(f"esto contiene la variable texto {texto} osi osi")
    #    return super().dispatch(request, *args, **kwargs)
