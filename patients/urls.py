from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet,
    StatutMaladieViewSet,
    TypeAnalyseViewSet,
    MaladieViewSet,
    ResultatAnalyseViewSet,
    NotePatientViewSet,
    RappelPatientViewSet
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'statuts-maladie', StatutMaladieViewSet)
router.register(r'types-analyse', TypeAnalyseViewSet)
router.register(r'maladies', MaladieViewSet)
router.register(r'resultats-analyse', ResultatAnalyseViewSet)
router.register(r'notes-patients', NotePatientViewSet)
router.register(r'rappels-patients', RappelPatientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]