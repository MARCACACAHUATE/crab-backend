from django.urls import path, include
from rest_framework.routers import DefaultRouter

from datasets import views

router = DefaultRouter()
router.register(r'datasets', views.DatasetViewSet, basename="dataset")

urlpatterns = [
        path('', include(router.urls))
    ]
