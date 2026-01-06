from django.db import models

class ModeConsultation(models.Model):
    nom_mode = models.CharField(max_length=50)  # Présentiel, Téléconsultation

    def __str__(self):
        return self.nom_mode

class StatutRdv(models.Model):
    nom_statut = models.CharField(max_length=50)  # Confirmé, Annulé, etc.

    def __str__(self):
        return self.nom_statut

class RendezVous(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    medecin = models.ForeignKey('medecins.Medecin', on_delete=models.CASCADE)
    centre = models.ForeignKey('centres.CentreSante', on_delete=models.CASCADE)
    mode_consultation = models.ForeignKey(ModeConsultation, on_delete=models.SET_NULL, null=True)
    statut_rdv = models.ForeignKey(StatutRdv, on_delete=models.SET_NULL, null=True)
    date_heure = models.DateTimeField()

    def __str__(self):
        return f"RDV {self.patient} → {self.medecin} le {self.date_heure.date()}"