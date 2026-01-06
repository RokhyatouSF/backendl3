from rest_framework import viewsets
from .models import (
    Patient, Maladie, StatutMaladie, TypeAnalyse,
    ResultatAnalyse, NotePatient, RappelPatient
)
from .serializers import (
    PatientSerializer, MaladieSerializer, StatutMaladieSerializer,
    TypeAnalyseSerializer, ResultatAnalyseSerializer,
    NotePatientSerializer, RappelPatientSerializer
)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class StatutMaladieViewSet(viewsets.ModelViewSet):
    queryset = StatutMaladie.objects.all()
    serializer_class = StatutMaladieSerializer


class TypeAnalyseViewSet(viewsets.ModelViewSet):
    queryset = TypeAnalyse.objects.all()
    serializer_class = TypeAnalyseSerializer


class MaladieViewSet(viewsets.ModelViewSet):
    queryset = Maladie.objects.all()
    serializer_class = MaladieSerializer


class ResultatAnalyseViewSet(viewsets.ModelViewSet):
    queryset = ResultatAnalyse.objects.all()
    serializer_class = ResultatAnalyseSerializer


class NotePatientViewSet(viewsets.ModelViewSet):
    queryset = NotePatient.objects.all()
    serializer_class = NotePatientSerializer


class RappelPatientViewSet(viewsets.ModelViewSet):
    queryset = RappelPatient.objects.all()
    serializer_class = RappelPatientSerializer