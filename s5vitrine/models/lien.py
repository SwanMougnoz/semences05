from django.db import models


class Lien(models.Model):
    viewname = models.CharField(max_length=255)
    params = models.CharField(max_length=255)

    class Meta:
        unique_together = ('viewname', 'params')
