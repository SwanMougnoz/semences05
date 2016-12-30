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


class EntretientQuerySet(models.query.QuerySet):
    def accepte(self):
        return self.filter(accepte=True)


class EntretientManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return EntretientQuerySet(self.model)

    def accepte(self):
        return self.get_queryset().accepte()


class Entretient(models.Model):
    jardin = models.ForeignKey(Jardin, on_delete=models.CASCADE)
    adherant = models.ForeignKey(Adherant, on_delete=models.CASCADE)
    accepte = models.BooleanField(default=False)

    objects = EntretientManager()
