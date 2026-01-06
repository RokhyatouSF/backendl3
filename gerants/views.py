from rest_framework import viewsets
from .models import Gerant
from .serializers import GerantSerializer

class GerantViewSet(viewsets.ModelViewSet):
    queryset = Gerant.objects.all()
    serializer_class = GerantSerializer