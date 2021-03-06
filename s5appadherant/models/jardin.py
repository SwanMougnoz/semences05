# -*- coding: utf-8 -*-
from ckeditor.fields import RichTextField
from django.db import models
from s5appadherant.models import Adherant, Adresse


class Jardin(models.Model):
    proprietaire = models.ForeignKey(Adherant, on_delete=models.CASCADE)
    adresse = models.ForeignKey(Adresse, on_delete=models.CASCADE)
    appelation = models.CharField(max_length=255)
    exposition = models.CharField(max_length=255)
    type_sol = models.CharField(max_length=255)
    irrigation = models.CharField(max_length=255)
    mise_en_culture = models.IntegerField()
    description = RichTextField()
    short_description = models.CharField(max_length=255, null=True, blank=True, verbose_name='Résumé')
    superficie = models.FloatField(verbose_name='Superficie (en m²)')

    def __unicode__(self):
        return self.appelation

