from django.forms import ModelForm
from s5appadherant.models import Variete


class VarieteForm(ModelForm):
    class Meta:
        model = Variete
        exclude = []
