from rest_framework import serializers
from .models import User, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'nom_role']

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    genre_display = serializers.CharField(source='get_genre_display', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'telephone', 
                  'role', 'date_naissance', 'photo_profil', 'email_verified', 'phone_verified', 'genre_display']
        read_only_fields = ['id', 'email_verified', 'phone_verified']