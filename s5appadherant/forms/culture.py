# -*- coding: utf-8 -*-
from django import forms

from s5appadherant.models import Culture


class CultureForm(forms.ModelForm):
    class Meta:
        model = Culture
        exclude = ['date_fin', 'jardin']


