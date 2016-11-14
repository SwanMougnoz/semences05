from django.db import models
from s5vitrine.models import Menuitem


class PageContenu(models.Model):
    titre_page = models.CharField(max_length=255)
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    menuitem = models.OneToOneField(
        Menuitem,
        on_delete=models.CASCADE
    )
