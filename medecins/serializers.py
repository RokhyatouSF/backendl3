from rest_framework import serializers
from .models import Medecin

class MedecinSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Affiche prénom + nom

    class Meta:
        model = Medecin
        fields = '__all__'