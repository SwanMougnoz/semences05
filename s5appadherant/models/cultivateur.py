from django.db import models

from s5appadherant.managers.cultivateur import CultivateurManager
from s5appadherant.models import Jardin, Adherant


class Cultivateur(models.Model):
    jardin = models.ForeignKey(Jardin, on_delete=models.CASCADE)
    adherant = models.ForeignKey(Adherant, on_delete=models.CASCADE)
    accepte = models.BooleanField(default=False)

    objects = CultivateurManager()
