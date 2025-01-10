from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class BenutzerProfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    date_of_birth = models.DateField( null=True, blank=True)
    profil_image = models.ImageField(upload_to='profil_images/', null=True, blank=True)
    some_file = models.FileField(upload_to='some_files/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profil"