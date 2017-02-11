# -*- coding: utf-8 -*-
import datetime

from actstream import action
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import View
from rules.contrib.views import PermissionRequiredMixin
from table.views import FeedDataView

from s5appadherant.forms.culture import CultureForm
from s5appadherant.models import Culture, Jardin
from s5appadherant.tables.culture import CultureTable, CultureTableCultivateur
from s5appadherant import permissions


class CultureDataView(FeedDataView, PermissionRequiredMixin):

    def get(self, request, *args, **kwargs):
        self.jardin = get_object_or_404(Jardin, pk=kwargs.get('jardin_id'))

        if request.user.has_perm('s5appadherant.change_jardin', self.jardin):
            self.token = CultureTableCultivateur.token
        else:
            self.token = CultureTable.token

        return super(CultureDataView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Culture.objects.filter(jardin=self.jardin, date_fin__isnull=True)


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
            culture.date_debut = form.cleaned_data['date_debut']
            culture.save()

            action.send(request.user, verb='add', action_object=culture, target=jardin)

            return redirect('s5appadherant:jardin_detail', jardin_id=jardin.id)

        return self.render_to_response({
            'jardin': jardin,
            'form': form,
            'menu_actif': 'jardin',
            'titre_page': u"Ajout d'une variété cultivée"
        })


class CultureDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 's5appadherant.change_jardin'

    def get_permission_object(self):
        return get_object_or_404(Jardin, pk=self.kwargs['jardin_id'])

    def get(self, request, *args, **kwargs):
        culture = get_object_or_404(Culture, pk=kwargs['culture_id'])
        jardin = get_object_or_404(Jardin, pk=kwargs['jardin_id'])

        if culture.date_fin is not None:
            return HttpResponseForbidden()

        if jardin != culture.jardin:
            return HttpResponseForbidden()

        culture.date_fin = datetime.date.today()
        culture.save()

        action.send(request.user, verb='delete', action_object=culture, target=jardin)

        return redirect('s5appadherant:jardin_detail', jardin_id=jardin.id)
