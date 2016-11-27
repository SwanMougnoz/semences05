from django.db import models


class Variete(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(null=True)
    photo = models.ImageField(upload_to='varietes', null=True)
