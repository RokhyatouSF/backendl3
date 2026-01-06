from rest_framework import viewsets
from .models import Medecin
from .serializers import MedecinSerializer

class MedecinViewSet(viewsets.ModelViewSet):
    queryset = Medecin.objects.all()
    serializer_class = MedecinSerializer