from rest_framework import serializers
from .models import (
    Patient, Maladie, StatutMaladie, TypeAnalyse,
    ResultatAnalyse, NotePatient, RappelPatient
)

class PatientSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Affiche le nom/prénom de l'utilisateur

    class Meta:
        model = Patient
        fields = '__all__'


class StatutMaladieSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatutMaladie
        fields = '__all__'


class TypeAnalyseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeAnalyse
        fields = '__all__'


class MaladieSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    statut = serializers.StringRelatedField()  # Si vous avez ajouté le champ statut
    resultat_analyse = serializers.StringRelatedField(allow_null=True)

    class Meta:
        model = Maladie
        fields = '__all__'


class ResultatAnalyseSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    type_analyse = serializers.StringRelatedField()

    class Meta:
        model = ResultatAnalyse
        fields = '__all__'


class NotePatientSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()

    class Meta:
        model = NotePatient
        fields = '__all__'


class RappelPatientSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()

    class Meta:
        model = RappelPatient
        fields = '__all__'