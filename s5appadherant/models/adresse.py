from django.db import models


class Adresse(models.Model):
    adresse = models.CharField(max_length=255)
    commune = models.CharField(max_length=255)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    altitude = models.IntegerField(null=True)
