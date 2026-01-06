from rest_framework import serializers
from .models import ModeConsultation, StatutRdv, RendezVous

class ModeConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeConsultation
        fields = '__all__'


class StatutRdvSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatutRdv
        fields = '__all__'


class RendezVousSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    medecin = serializers.StringRelatedField()
    centre = serializers.StringRelatedField()
    mode_consultation = serializers.StringRelatedField(allow_null=True)
    statut_rdv = serializers.StringRelatedField(allow_null=True)

    class Meta:
        model = RendezVous
        fields = '__all__'