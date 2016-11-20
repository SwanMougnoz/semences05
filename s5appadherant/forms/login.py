from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=254, label='Utilisateur')
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')
