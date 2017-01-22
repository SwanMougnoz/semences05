# coding=utf-8
from ckeditor.fields import RichTextField
from django.db import models
import uuid
import os


def get_variete_upload_path(instance, filename):
    # todo: trouver une solution pour ne pas garder les ancien fichier quand on change la photo
    original_filename, extension = os.path.splitext(filename)
    unique_filename = str(uuid.uuid4().hex)
    filepath = 'varietes/{0}{1}'.format(unique_filename, extension)
    return filepath


class Variete(models.Model):
    nom = models.CharField(max_length=255)
    description = RichTextField(null=True)
    short_description = models.CharField(max_length=255, null=True, blank=True, verbose_name='Résumé')
    photo = models.ImageField(upload_to=get_variete_upload_path, null=True, blank=True)
    date_ajout = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.nom

