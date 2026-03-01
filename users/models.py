from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password, check_password


class Role(models.Model):
    nom_role = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"

    def __str__(self):
        return self.nom_role


class User(AbstractUser):
    GENRE_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )

    telephone = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\+221(77|78|76|75|70)\d{7}$',
                message="Numéro sénégalais invalide"
            )
        ]
    )

    date_naissance = models.DateField(null=True, blank=True)

    genre = models.CharField(
        max_length=1,
        choices=GENRE_CHOICES,
        null=True,
        blank=True
    )

    piece_identite_numero = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )

    def set_piece_identite_numero(self, raw_number):
        """Hash le numéro avant sauvegarde"""
        if raw_number:
            self.piece_identite_numero = make_password(raw_number)
        else:
            self.piece_identite_numero = None

    def check_piece_identite_numero(self, raw_number):
        """Vérifie si le numéro correspond au hash"""
        if not self.piece_identite_numero:
            return False
        return check_password(raw_number, self.piece_identite_numero)

    document_piece_identite = models.ImageField(
        upload_to='pieces_identite/',
        null=True,
        blank=True
    )

    id_verified = models.BooleanField(default=False)

    id_verification_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'En attente'),
            ('approved', 'Approuvé'),
            ('rejected', 'Rejeté'),
            ('manual', 'Vérification manuelle'),
        ],
        default='pending'
    )

    photo_profil = models.ImageField(
        upload_to='profils/',
        null=False,
        blank=False,
        default='profils/default.png'
    )

    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)  # 🔥 PAS TRUE

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['email', 'telephone']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.telephone})"
