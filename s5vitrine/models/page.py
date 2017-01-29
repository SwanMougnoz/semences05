# coding=utf-8
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models


class PageContenu(models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField()

    @property
    def url(self):
        try:
            url = reverse('s5vitrine:contenu', args=[self.id])
        except NoReverseMatch:
            url = None
        return url

    def __unicode__(self):
        return self.titre

    class Meta:
        verbose_name = 'Page de contenu'
        verbose_name_plural = 'Pages de contenu'


class PageGenerique(models.Model):
    viewname = models.CharField(max_length=255)
    params = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, default='special_page')

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

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Page spéciale'
        verbose_name_plural = 'Pages spéciales'
