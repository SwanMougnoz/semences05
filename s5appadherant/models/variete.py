from django.db import models


class Variete(models.Model):
    nom = models.CharField(max_length=255, null=False)
    description = models.TextField()
    photo = models.URLField()