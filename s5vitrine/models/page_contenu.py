from django.db import models
from s5vitrine.models import Lien


class PageContenu(models.Model):
    titre_page = models.CharField(max_length=255)
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    lien_menu = models.OneToOneField(
        Lien,
        on_delete=models.CASCADE,
        null=True
    )
