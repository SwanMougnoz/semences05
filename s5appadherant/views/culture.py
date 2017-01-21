# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rules.contrib.views import PermissionRequiredMixin
from table.views import FeedDataView

from s5appadherant.forms.culture import CultureForm
from s5appadherant.models import Culture, Jardin
from s5appadherant.tables.culture import CultureTable
from s5appadherant import permissions


class CultureDataView(FeedDataView, PermissionRequiredMixin):
    token = CultureTable.token

    def get_queryset(self):
        jardin_id = self.kwargs.get('jardin_id')
        jardin = Jardin.objects.get(pk=jardin_id)
        return Culture.objects.filter(jardin=jardin)


class CultureAddView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 's5appadherant/culture/add.html'
    permission_required = 's5appadherant.change_jardin'

    def get_permission_object(self):
        jardin_id = self.kwargs.get('jardin_id')
        try:
            jardin = Jardin.objects.get(pk=jardin_id)
        except ObjectDoesNotExist:
            raise Http404
        return jardin

    def get(self, request, *args, **kwargs):
        jardin = Jardin.objects.get(pk=kwargs.get('jardin_id'))
        form = kwargs.get('form', CultureForm())

        return self.render_to_response({
            'jardin': jardin,
            'form': form,
            'menu_actif': 'jardin',
            'titre_page': u"Ajout d'une variété cultivée"
        })

    def post(self, request, **kwargs):
        jardin = Jardin.objects.get(pk=kwargs.get('jardin_id'))
        form = CultureForm(request.POST, request.FILES)

        if form.is_valid():
            variete = form.cleaned_data['variete']
            variete.save()

            culture = Culture()
            culture.jardin = jardin
            culture.variete = variete
            culture.type_conservation = form.cleaned_data['type_conservation']
            culture.save()

            return redirect('s5appadherant:jardin_detail', jardin_id=jardin.id)

        return self.render_to_response({
            'jardin': jardin,
            'form': form,
            'menu_actif': 'jardin',
            'titre_page': u"Ajout d'une variété cultivée"
        })
