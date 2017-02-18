# coding=utf-8
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from s5appadherant.models import Jardin, Adresse


class JardinForm(forms.ModelForm):

    class Meta:
        model = Jardin
        exclude = ['proprietaire', 'adresse']
        widgets = {
            'exposition': forms.TextInput(attrs={'placeholder': 'ex: nord-est'}),
            'type_sol': forms.TextInput(attrs={'placeholder': 'ex: limoneux'}),
            'irrigation': forms.TextInput(attrs={'placeholder': 'ex: goutte à goutte'}),
            'mise_en_culture': forms.TextInput(attrs={'placeholder': 'ex: 2016'}),
            'superficie': forms.TextInput(attrs={'placeholder': 'ex: 250'}),
            'description': CKEditorWidget(config_name='restricted'),
            'short_description': forms.TextInput(attrs={'placeholder': 'Facultatif: dévrivez en quelques mots ce jardin'})
        }

