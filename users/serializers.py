from rest_framework import serializers
from .models import User, Role
from django.contrib.auth.password_validation import validate_password


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'nom_role']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        required=True
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'telephone',
            'first_name', 'last_name',
            'date_naissance', 'genre',
            'password', 'password2', 'role'
        ]
        extra_kwargs = {
            'username': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Les mots de passe ne correspondent pas."
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        # ✅ GÉNÉRATION AUTOMATIQUE DU USERNAME
        if not validated_data.get('username'):
            email = validated_data.get('email')
            telephone = validated_data.get('telephone')

            validated_data['username'] = (
                email.split('@')[0] if email else telephone
            )

        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'telephone',
            'first_name', 'last_name',
            'date_naissance', 'genre', 'role',
            'photo_profil',
            'email_verified', 'phone_verified',
            'id_verified', 'id_verification_status'
        ]
        read_only_fields = [
            'id',
            'email_verified',
            'phone_verified',
            'id_verified',
            'id_verification_status'
        ]
