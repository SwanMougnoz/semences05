# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class Adherant(models.Model):
    EXPERIENCE_ENUM = (
        ('debutant', 'Débutant'),
        ('confirme', 'Confirmé')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=10, null=True)
    est_professionnel = models.BooleanField(default=False)
    experience = models.CharField(max_length=32, choices=EXPERIENCE_ENUM)
