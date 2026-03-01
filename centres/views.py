from rest_framework import viewsets
from .models import TypeCentre, Specialite, CentreSante, MedecinCentre
from .serializers import (
    TypeCentreSerializer, SpecialiteSerializer,
    CentreSanteSerializer, MedecinCentreSerializer
)
from django.db.models import Count

class TypeCentreViewSet(viewsets.ModelViewSet):
    queryset = TypeCentre.objects.all()
    serializer_class = TypeCentreSerializer


class SpecialiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialite.objects.annotate(
        nombre_medecins=Count('medecincentre')
    )
    serializer_class = SpecialiteSerializer


class CentreSanteViewSet(viewsets.ModelViewSet):
    queryset = CentreSante.objects.all()
    serializer_class = CentreSanteSerializer


class MedecinCentreViewSet(viewsets.ModelViewSet):
    queryset = MedecinCentre.objects.all()
    serializer_class = MedecinCentreSerializer