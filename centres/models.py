from django.db import models

class TypeCentre(models.Model):
    nom_type = models.CharField(max_length=100)

    def __str__(self):
        return self.nom_type

class Specialite(models.Model):
    nom_specialite = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.nom_specialite

class CentreSante(models.Model):
    gerant = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='centres_geres')
    type_centre = models.ForeignKey(TypeCentre, on_delete=models.SET_NULL, null=True)
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    adresse = models.CharField(max_length=300)
    localisation_lat = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    localisation_lng = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    numero_identification_ministere = models.CharField(max_length=100, blank=True)
    email_contact = models.EmailField(blank=True)
    telephone_contact = models.CharField(max_length=20)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom

class MedecinCentre(models.Model):
    medecin = models.ForeignKey('medecins.Medecin', on_delete=models.CASCADE)
    centre = models.ForeignKey(CentreSante, on_delete=models.CASCADE)
    specialite = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('medecin', 'centre', 'specialite')

    def __str__(self):
        return f"{self.medecin} @ {self.centre} - {self.specialite}"