from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, max_length=254, label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')
