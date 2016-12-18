from django import forms
from s5appadherant.models import Jardin, Adresse


class JardinForm(forms.ModelForm):
    adresse = forms.CharField(max_length=255)
    commune = forms.CharField(max_length=255)
    latitude = forms.FloatField()
    longitude = forms.FloatField()
    altitude = forms.IntegerField()

    def save(self, commit=True):
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
