from django.db import models
from s5vitrine.models import Lien


class Menuitem(models.Model):
    """
    Elements du menu principal
    """
    label = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255)
    position = models.IntegerField()
    lien = models.ForeignKey(
        Lien,
        on_delete=models.CASCADE
    )

