# -*- coding: utf-8 -*-
from django.db import models
from s5appadherant.models import Adherant, Adresse


class Jardin(models.Model):
    proprietaire = models.ForeignKey(Adherant, on_delete=models.CASCADE)
    adresse = models.ForeignKey(Adresse, on_delete=models.CASCADE)
    appelation = models.CharField(max_length=255)
    exposition = models.IntegerField()
    type_sol = models.CharField(max_length=255)
    irrigation = models.CharField(max_length=255)
    mise_en_culture = models.IntegerField()
    description = models.TextField()
    superficie = models.FloatField()

    def __str__(self):
        return self.appelation

