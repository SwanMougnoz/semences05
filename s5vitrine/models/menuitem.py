from django.db import models


class Menuitem(models.Model):
    """
    Elements du menu principal
    """
    identifier = models.CharField(max_length=255, primary_key=True)
    label = models.CharField(max_length=255)
    position = models.IntegerField()
    active = models.BooleanField(default=False)
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

