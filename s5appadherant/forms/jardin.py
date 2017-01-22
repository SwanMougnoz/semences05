from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from s5appadherant.models import Jardin, Adresse


class JardinForm(forms.ModelForm):
    adresse = forms.CharField(max_length=255)
    commune = forms.CharField(max_length=255)
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    altitude = forms.IntegerField()
    description = forms.CharField(widget=CKEditorWidget(config_name='restricted'))

    def __init__(self, *args, **kwargs):
        super(JardinForm, self).__init__(*args, **kwargs)
        self.set_initial(kwargs.pop('instance'))

    def set_initial(self, jardin):
        if isinstance(jardin, Jardin):
            self.fields['adresse'].initial = jardin.adresse.adresse
            self.fields['commune'].initial = jardin.adresse.commune
            self.fields['latitude'].initial = jardin.adresse.latitude
            self.fields['longitude'].initial = jardin.adresse.longitude
            self.fields['altitude'].initial = jardin.adresse.altitude

    def save(self, commit=True):
        try:
            adr = self.instance.adresse
        except ObjectDoesNotExist:
            adr = Adresse()

        adr.adresse = self.cleaned_data.get('adresse')
        adr.commune = self.cleaned_data.get('commune')
        adr.latitude = self.cleaned_data.get('latitude')
        adr.longitude = self.cleaned_data.get('longitude')
        adr.altitude = self.cleaned_data.get('altitude')
        adr.save()

        self.instance.adresse = adr
        return super(forms.ModelForm, self).save(commit=commit)

    class Meta:
        model = Jardin
        exclude = ['proprietaire', 'adresse']
