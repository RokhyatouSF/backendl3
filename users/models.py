from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    nom_role = models.CharField(max_length=50, unique=True)  # Patient, Médecin, Gérant

    def __str__(self):
        return self.nom_role

    class Meta:
        verbose_name_plural = "Rôles"

class User(AbstractUser):
    GENRE_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    )
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    telephone = models.CharField(max_length=20, unique=True)
    date_naissance = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES, blank=True, null=True)
    piece_identite_numero = models.CharField(max_length=50, blank=True, null=True)
    document_piece_identite = models.ImageField(
        upload_to='pieces_identite/',
        blank=True,
        null=True,
        verbose_name="Pièce d'identité"
    )
    id_verified = models.BooleanField(
        default=False,
        verbose_name="Identité vérifiée"
    )
    id_verification_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'En attente'),
            ('approved', 'Approuvé'),
            ('rejected', 'Rejeté'),
            ('manual', 'Vérification manuelle')
        ],
        default='pending'
    )    
    photo_profil = models.ImageField(upload_to='profils/', blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['email', 'telephone']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.telephone})"