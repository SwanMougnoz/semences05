from django import forms

from s5appadherant.models import Adresse


class AdresseForm(forms.ModelForm):
    class Meta:
        model = Adresse
        exclude = []
