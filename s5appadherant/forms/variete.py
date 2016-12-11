from django import forms
from s5appadherant.models import Variete


class VarieteForm(forms.ModelForm):

    photo = forms.ImageField(required=False)

    class Meta:
        model = Variete
        exclude = []
