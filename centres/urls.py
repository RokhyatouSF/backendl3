from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TypeCentreViewSet, SpecialiteViewSet,
    CentreSanteViewSet, MedecinCentreViewSet
)

router = DefaultRouter()
router.register(r'types-centre', TypeCentreViewSet)
router.register(r'specialites', SpecialiteViewSet)
router.register(r'centres-sante', CentreSanteViewSet)
router.register(r'medecins-centres', MedecinCentreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]