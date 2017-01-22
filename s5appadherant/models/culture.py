# -*- coding: utf-8 -*-
from django.db import models

from s5appadherant.models import Jardin, Variete


class Culture(models.Model):
    CONSERVATION_ENUM = (
        ('dynamique', 'Dynamique'),
        ('conservatoire', 'Conservatoire')
    )

    jardin = models.ForeignKey(Jardin, on_delete=models.CASCADE)
    variete = models.ForeignKey(Variete, on_delete=models.CASCADE)
    type_conservation = models.CharField(max_length=255, choices=CONSERVATION_ENUM)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True)

