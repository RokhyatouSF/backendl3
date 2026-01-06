from rest_framework import serializers
from .models import Gerant

class GerantSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Gerant
        fields = '__all__'