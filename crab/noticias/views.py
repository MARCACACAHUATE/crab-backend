from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny

from noticias.serializers import ListNoticiaSerializer
from .models import Noticia


class NoticiaViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Noticia.objects.all()
    serializer_class = ListNoticiaSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["categorias"] = []
        return context

    def get_permissions(self):
        if self.action == "destroy":
            permissions = [IsAdminUser]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]
    
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
