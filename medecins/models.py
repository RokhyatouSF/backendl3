from django.db import models

class Medecin(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='profil_medecin')

    def __str__(self):
        return f"Dr {self.user.get_full_name()}"