from django import forms
from django.contrib.auth.models import User

from s5appadherant.models import Adherant


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = []


class AdherantForm(forms.ModelForm):
    class Meta:
        model = Adherant
        exclude = []
