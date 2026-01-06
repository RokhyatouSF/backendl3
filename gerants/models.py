from django.db import models

class Gerant(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='profil_gerant')

    def __str__(self):
        return f"Gérant: {self.user.get_full_name()}"