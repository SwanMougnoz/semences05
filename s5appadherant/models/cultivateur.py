from django.db import models

from s5appadherant.models import Jardin, Adherant


class CultivateurQuerySet(models.query.QuerySet):
    def accepte(self):
        return self.filter(accepte=True)


class CultivateurManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return CultivateurQuerySet(self.model)

    def accepte(self):
        return self.get_queryset().accepte()


class Cultivateur(models.Model):
    jardin = models.ForeignKey(Jardin, on_delete=models.CASCADE)
    adherant = models.ForeignKey(Adherant, on_delete=models.CASCADE)
    accepte = models.BooleanField(default=False)

    objects = CultivateurManager()
