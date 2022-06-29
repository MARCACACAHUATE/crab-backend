from django.urls import path, include
from rest_framework.routers import DefaultRouter
from noticias import views


router = DefaultRouter()
router.register(r'noticias', views.NoticiaViewSet, basename='noticia')

urlpatterns = [
    path('', include(router.urls))
]
