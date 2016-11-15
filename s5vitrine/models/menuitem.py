from django.db import models
from django.apps import apps


class Menuitem(models.Model):
    """
    Elements du menu principal
    """
    identifiant = models.CharField(max_length=255, primary_key=True)
    libelle = models.CharField(max_length=255)
    position = models.IntegerField()
    actif = models.BooleanField(default=False)
    _page_contenu = models.OneToOneField(
        's5vitrine.PageContenu',
        on_delete=models.CASCADE,
        null=True
    )
    _page_generique = models.OneToOneField(
        's5vitrine.PageGenerique',
        on_delete=models.CASCADE,
        null=True
    )

    @property
    def page(self):
        if self._page_contenu is not None:
            return self._page_contenu
        elif self._page_generique is not None:
            return self._page_generique
        else:
            return None

    @page.setter
    def page(self, value):
        if isinstance(value, apps.get_model(app_label='s5vitrine', model_name='PageGenerique')):
            self._page_generique = value
            self._page_contenu = None
        elif isinstance(value, apps.get_model(app_label='s5vitrine', model_name='PageContenu')):
            self._page_contenu = value
            self._page_generique = None
        else:
            msg = "Menuitem.page reference soit une PageContenu soit une PageGenerique. %s obtenu" % value.__class__
            raise ValueError(msg)
