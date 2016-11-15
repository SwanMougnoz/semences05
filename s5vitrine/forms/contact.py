from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    objet = forms.CharField(required=True, max_length=255)
    message = forms.CharField(required=True, widget=forms.Textarea)

