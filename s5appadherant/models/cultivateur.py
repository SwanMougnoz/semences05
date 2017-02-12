from django.db import models

from s5appadherant.managers.cultivateur import CultivateurManager
from s5appadherant.models import Jardin, Adherant


class Cultivateur(models.Model):
    jardin = models.ForeignKey(Jardin, on_delete=models.CASCADE)
    adherant = models.ForeignKey(Adherant, on_delete=models.CASCADE)
    accepte = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)

    objects = CultivateurManager()

    def accept(self):
        self.accepte = True
        self.pending = False
        self.save()

    def deny(self):
        self.accepte = False
        self.pending = False
        self.save()

