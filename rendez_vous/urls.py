from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ModeConsultationViewSet, StatutRdvViewSet, RendezVousViewSet

router = DefaultRouter()
router.register(r'modes-consultation', ModeConsultationViewSet)
router.register(r'statuts-rdv', StatutRdvViewSet)
router.register(r'rendez-vous', RendezVousViewSet)

urlpatterns = [
    path('', include(router.urls)),
]