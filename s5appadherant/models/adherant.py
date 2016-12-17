# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from s5appadherant.models import Adresse


class AdherantManager(models.Manager):
    def get_from_user(self, user):
        return self.filter(user=user)


class Adherant(models.Model):
    EXPERIENCE_ENUM = (
        ('debutant', 'Débutant'),
        ('confirme', 'Confirmé')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adresse = models.ForeignKey(Adresse, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=10, null=True)
    est_professionnel = models.BooleanField(default=False)
    experience = models.CharField(max_length=32, choices=EXPERIENCE_ENUM)

    objects = AdherantManager()
