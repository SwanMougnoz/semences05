from django.db import models


class Menuitem(models.Model):
    libelle = models.CharField(max_length=255)
    position = models.IntegerField()
    lien = models.URLField()

