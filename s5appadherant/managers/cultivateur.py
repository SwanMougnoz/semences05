from django.db import models


class CultivateurQuerySet(models.query.QuerySet):
    def accepte(self):
        return self.filter(accepte=True)


class CultivateurManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return CultivateurQuerySet(self.model)

    def accepte(self):
        return self.get_queryset().accepte()