from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from .models import User, Role

import re

SENEGAL_PHONE_REGEX = r'^\+221(77|78|76|75|70)\d{7}$'
from .models import User




from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        print("🔵 JWT ATTRS :", attrs)

        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email=email)
            print("✅ USER TROUVÉ :", user.username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Email ou mot de passe incorrect")

        if not user.check_password(password):
            raise serializers.ValidationError("Email ou mot de passe incorrect")

        if not user.is_active:
            raise serializers.ValidationError("Compte désactivé")

        # 🔥 GÉNÉRATION MANUELLE DU TOKEN
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.nom_role if user.role else None
            }
        }



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'nom_role']


class RegisterSerializer(serializers.ModelSerializer):
    photo_profil = serializers.ImageField(required=True)

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True)

    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        required=True
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'telephone',
            'first_name',
            'last_name',
            'date_naissance',
            'genre',
            'password',
            'password2',
            'role',
            'photo_profil'
        ]
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': True},
            'telephone': {'required': True},
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError(
                {"password": "Les mots de passe ne correspondent pas."}
            )

        email = attrs.get('email')
        telephone = attrs.get('telephone')

        if not email or not telephone:
            raise serializers.ValidationError("Email ET téléphone requis.")

        if User.objects.filter(Q(email=email) | Q(telephone=telephone)).exists():
            raise serializers.ValidationError("Email ou téléphone déjà utilisé.")

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        if not validated_data.get('username'):
            validated_data['username'] = validated_data['email'].split('@')[0]

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            telephone=validated_data.get('telephone'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            date_naissance=validated_data.get('date_naissance'),
            genre=validated_data.get('genre'),
            role=validated_data.get('role'),
            photo_profil=validated_data.get('photo_profil'),
        )

        user.email_verified = False
        user.phone_verified = False
        user.is_active = True
        user.save()

        return user

    def validate_telephone(self, value):
        if not re.match(SENEGAL_PHONE_REGEX, value):
            raise serializers.ValidationError(
                "Numéro sénégalais invalide. Format attendu : +22177XXXXXXX"
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'telephone',
            'first_name',
            'last_name',
            'date_naissance',
            'genre',
            'role',
            'photo_profil',
            'email_verified',
            'phone_verified',
            'id_verified',
            'id_verification_status'
        ]
        read_only_fields = [
            'id',
            'email_verified',
            'phone_verified',
            'id_verified',
            'id_verification_status'
        ]

from centres.models import Specialite

class SpecialiteSerializer(serializers.ModelSerializer):
    nombre_medecins = serializers.IntegerField(read_only=True)

    class Meta:
        model = Specialite
        fields = [
            'id',
            'nom_specialite',
            'description_specialite',
            'nombre_medecins'
        ]
