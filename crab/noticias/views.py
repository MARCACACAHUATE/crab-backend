from rest_framework import mixins, viewsets, status
from rest_framework.response import Response


from noticias.serializers import CreateNoticiaSerializer, ListNoticiaSerializer
from .models import Noticia, Categoria, Pagina


class NoticiaViewSet(viewsets.GenericViewSet):
    queryset = Noticia.objects.all()
    serializer_class = ListNoticiaSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["categorias"] = []
        return context
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "message": "Noticias almacenadas con exito",
            "data": {
                "total_noticias": len(serializer.data["noticias"])
                }
            }
        return Response(data, status=status.HTTP_201_CREATED)
