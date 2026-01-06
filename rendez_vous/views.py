from rest_framework import viewsets
from .models import ModeConsultation, StatutRdv, RendezVous
from .serializers import ModeConsultationSerializer, StatutRdvSerializer, RendezVousSerializer

class ModeConsultationViewSet(viewsets.ModelViewSet):
    queryset = ModeConsultation.objects.all()
    serializer_class = ModeConsultationSerializer


class StatutRdvViewSet(viewsets.ModelViewSet):
    queryset = StatutRdv.objects.all()
    serializer_class = StatutRdvSerializer


class RendezVousViewSet(viewsets.ModelViewSet):
    queryset = RendezVous.objects.all()
    serializer_class = RendezVousSerializer