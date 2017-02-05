# -*- coding: utf-8 -*-
import datetime
from functools import partial

from ckeditor.widgets import CKEditorWidget
from django import forms
from django.core.exceptions import ValidationError

from s5appadherant.models import Culture, Variete

DatePicker = partial(forms.DateInput, {'class': 'datepicker'})


class CultureForm(forms.Form):
    variete = forms.ModelChoiceField(label="Variété", queryset=Variete.objects.all(), required=False)
    type_conservation = forms.ChoiceField(label="Type de conservation", choices=Culture.CONSERVATION_ENUM)
    date_debut = forms.DateField(label="Mise en culture", widget=DatePicker(), initial=datetime.date.today())
    variete_nom = forms.CharField(label="Nom", max_length=255, required=False)
    variete_description = forms.CharField(label="Description",
                                          widget=CKEditorWidget(config_name='restricted'),
                                          required=False)
    variete_photo = forms.ImageField(label="Photo", required=False)

    def clean(self):
        """
        On s'assure que si aucune variété n'a été choisie, les champs nécessaire à la création d'une nouvelle
        on été remplis
        :return:
        """
        variete = self.cleaned_data['variete']

        if variete is None:
            if not self.cleaned_data['variete_nom']:
                raise ValidationError("Veuillez choisir une variété dans la liste ou en créer une nouvelle")

            variete = Variete()
            variete.nom = self.cleaned_data['variete_nom']
            variete.description = self.cleaned_data['variete_description']
            variete.photo = self.cleaned_data['variete_photo']

        self.cleaned_data['variete'] = variete

