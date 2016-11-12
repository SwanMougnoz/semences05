from django.db import models


class Menuitem(models.Model):
    label = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255)
    position = models.IntegerField()
    lien = models.URLField()

