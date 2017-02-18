from django import forms
from django.contrib.auth.models import User

from s5appadherant.models import Adherant


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['date_joined',
                   'is_active',
                   'is_staff',
                   'is_superuser',
                   'last_login',
                   'user_permissions',
                   'groups',
                   'password',
                   'username']


class AdherantForm(forms.ModelForm):
    class Meta:
        model = Adherant
        exclude = ['user', 'adresse', 'processed_actions']
