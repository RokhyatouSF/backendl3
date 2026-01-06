from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedecinViewSet

router = DefaultRouter()
router.register(r'medecins', MedecinViewSet)

urlpatterns = [
    path('', include(router.urls)),
]