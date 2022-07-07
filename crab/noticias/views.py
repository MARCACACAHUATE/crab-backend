from datetime import date

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny

from noticias.serializers import ListNoticiaSerializer, NoticiaModelSerializer
from .models import Noticia


class NoticiaViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Noticia.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return ListNoticiaSerializer
        return NoticiaModelSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["categorias"] = []
        return context

    def get_queryset(self):
        queryset = Noticia.objects.all()
        fecha_fin = self.request.query_params.get("fecha_fin")
        fecha = self.request.query_params.get("fecha")

        if fecha_fin and fecha:
            queryset = queryset.filter(fecha__range=(fecha, fecha_fin))
        elif fecha_fin or fecha:
            fecha = fecha_fin or fecha
            queryset = queryset.filter(fecha=fecha)
        else: 
            queryset = queryset.filter(fecha=date.today().isoformat())
        return queryset

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
