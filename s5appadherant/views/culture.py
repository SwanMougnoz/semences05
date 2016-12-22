# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.views.generic import TemplateView

from s5appadherant.forms.culture import CultureForm
from s5appadherant.models import Culture, Jardin


class CultureAddView(LoginRequiredMixin, TemplateView):
    template_name = 's5appadherant/culture/add.html'

    def get(self, request, *args, **kwargs):
        jardin_id = kwargs.get('jardin_id')
        try:
            jardin = Jardin.objects.get(pk=jardin_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("<h1>La page demandee n'existe pas</h1>")

        form = kwargs.get('form', CultureForm())

        return self.render_to_response({
            'jardin': jardin,
            'form': form,
            'menu_actif': 'jardin',
            'titre_page': u"Ajout d'une variété cultivée"
        })

    def post(self, request, *args, **kwargs):
        jardin_id = kwargs.get('jardin_id')
        try:
            jardin = Jardin.objects.get(pk=jardin_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("<h1>La page demandee n'existe pas</h1>")

        form = CultureForm(request.POST, request.FILES)

        if form.is_valid():
            variete = form.cleaned_data['variete']
            variete.save()

            culture = Culture()
            culture.jardin = jardin
            culture.variete = variete
            culture.save()

            return redirect('s5appadherant:jardin_detail', jardin_id=jardin.id)

        return self.render_to_response({
            'jardin': jardin,
            'form': form,
            'menu_actif': 'jardin',
            'titre_page': u"Ajout d'une variété cultivée"
        })
