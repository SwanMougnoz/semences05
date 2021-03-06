# -*- coding: utf-8 -*-
from actstream.models import Action
from django.contrib.auth.models import User
from django.db import models
from s5appadherant.models import Adresse


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
    processed_actions = models.ManyToManyField(Action, related_name='adherant_has_proceed')

    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)
