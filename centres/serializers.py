from rest_framework import serializers
from .models import TypeCentre, Specialite, CentreSante, MedecinCentre

class TypeCentreSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeCentre
        fields = '__all__'


class SpecialiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialite
        fields = '__all__'


class CentreSanteSerializer(serializers.ModelSerializer):
    gerant = serializers.StringRelatedField(allow_null=True)  # Affiche nom + prénom du gérant
    type_centre = serializers.StringRelatedField(allow_null=True)

    class Meta:
        model = CentreSante
        fields = '__all__'


class MedecinCentreSerializer(serializers.ModelSerializer):
    medecin = serializers.StringRelatedField()
    centre = serializers.StringRelatedField()
    specialite = serializers.StringRelatedField(allow_null=True)

    class Meta:
        model = MedecinCentre
        fields = '__all__'