from ckeditor.widgets import CKEditorWidget
from django import forms
from s5appadherant.models.variete import Variete


class VarieteForm(forms.ModelForm):

    photo = forms.ImageField(required=False)
    description = forms.CharField(widget=CKEditorWidget(config_name='restricted'))

    class Meta:
        model = Variete
        exclude = []
