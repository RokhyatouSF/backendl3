from django.db import models

class Patient(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='profil_patient')
    nfc_id = models.CharField(max_length=100, blank=True, null=True)
    numero_carte = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Patient: {self.user.get_full_name()}"

class Maladie(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='maladies')
    nom_maladie = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    resultat_analyse = models.ForeignKey('ResultatAnalyse', on_delete=models.SET_NULL, null=True, blank=True)
    date_diagnostic = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom_maladie} ({self.patient})"

class StatutMaladie(models.Model):
    nom_statut = models.CharField(max_length=100)  # Fréquent, En cours, etc.

    def __str__(self):
        return self.nom_statut

class TypeAnalyse(models.Model):
    nom_type = models.CharField(max_length=150)  # Sang, Radio, etc.

    def __str__(self):
        return self.nom_type

class ResultatAnalyse(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='analyses')
    type_analyse = models.ForeignKey(TypeAnalyse, on_delete=models.SET_NULL, null=True)
    nom_analyse = models.CharField(max_length=200)
    date_analyse = models.DateField()
    fichier_document = models.FileField(upload_to='analyses/', blank=True, null=True)

    def __str__(self):
        return f"{self.nom_analyse} - {self.patient}"

class NotePatient(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='notes')
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} ({self.patient})"

class RappelPatient(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rappels')
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_heure = models.DateTimeField()

    def __str__(self):
        return f"{self.titre} - {self.date_heure}"