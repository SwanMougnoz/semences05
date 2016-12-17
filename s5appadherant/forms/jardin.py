from django import forms
from s5appadherant.models import Jardin


class JardinForm(forms.ModelForm):
    class Meta:
        model = Jardin
        exclude = ['proprietaire', 'adresse']

