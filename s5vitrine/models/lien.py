from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models


class Lien(models.Model):
    viewname = models.CharField(max_length=255)
    params = models.CharField(max_length=255, null=True)

    @property
    def url(self):
        try:
            args = []
            if self.params is not None:
                args = self.params.split(' ')
            url = reverse(self.viewname, args=args)
        except NoReverseMatch:
            url = None
        return url

    class Meta:
        unique_together = ('viewname', 'params')
