from django import forms

from s5appadherant.models import Adresse


class AdresseFullForm(forms.ModelForm):
    class Meta:
        model = Adresse
        exclude = []


class AdresseForm(forms.ModelForm):
    class Meta:
        model = Adresse
        exclude = ['latitude', 'longitude', 'altitude']
