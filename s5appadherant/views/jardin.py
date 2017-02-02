# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.views.generic import ListView, TemplateView
from django.views.generic import UpdateView
from rules.contrib.views import PermissionRequiredMixin

from s5appadherant.forms.jardin import JardinForm
from s5appadherant.models import Jardin, Adherant
from s5appadherant.tables.culture import CultureTable
from s5appadherant import permissions


class JardinListView(LoginRequiredMixin, ListView):
    template_name = 's5appadherant/jardin/list.html'
    model = Jardin
    paginate_by = 10
    list_identifier = 'all'

    def get_context_data(self, **kwargs):
        context = super(JardinListView, self).get_context_data(**kwargs)
        context.update({
            'jardins': context.get('page_obj'),
            'list': self.list_identifier,
            'menu_actif': 'jardin',
            'titre_page': u"Mes jardins"
        })
        return context


class JardinAdherantListView(JardinListView):
    list_identifier = 'adherant'

    def get_queryset(self):
        adherant = get_object_or_404(Adherant, pk=self.kwargs.get('adherant_id'))
        return Jardin.objects.filter(proprietaire=adherant)


class JardinCultivteurListView(JardinListView):
    list_identifier = 'cultivateur'

    def get_queryset(self):
        adherant = get_object_or_404(Adherant, pk=self.kwargs.get('adherant_id'))
        return Jardin.objects.filter(cultivateur__accepte=True, cultivateur__adherant=adherant)


class JardinDetailView(LoginRequiredMixin, TemplateView):
    template_name = 's5appadherant/jardin/detail.html'

    def get(self, request, *args, **kwargs):
        jardin_id = kwargs.get('jardin_id', None)
        try:
            jardin = Jardin.objects.get(pk=jardin_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("<h1>La page demandee n'existe pas</h1>")

        culture_table = CultureTable(jardin=jardin)

        qs = jardin.cultivateur_set.all()
        cultivateurs_all = [cultivateur.adherant for cultivateur in qs]
        cultivateurs_acceptes = [cultivateur.adherant for cultivateur in qs.filter(accepte=True)]

        return self.render_to_response({
            'jardin': jardin,
            'culture_table': culture_table,
            'cultivateurs_all': cultivateurs_all,
            'cultivateurs_acceptes': cultivateurs_acceptes,
            'menu_actif': 'jardin',
            'titre_page': u'Jardin - %s' % jardin.appelation
        })


class JardinAddView(LoginRequiredMixin, CreateView):
    template_name = 's5appadherant/jardin/edit.html'
    form_class = JardinForm
    model = Jardin

    def get_success_url(self):
        return reverse('s5appadherant:jardin_adherant', kwargs={
            'adherant_id': self.request.user.adherant.id
        })

    def get_context_data(self, **kwargs):
        context = super(JardinAddView, self).get_context_data(**kwargs)
        context.update({
            'menu_actif': 'jardin',
            'titre_page': u"Ajout d'un jardin"
        })
        return context

    def form_valid(self, form):
        jardin = form.save(commit=False)
        jardin.proprietaire = self.request.user.adherant
        jardin.save()

        return HttpResponseRedirect(self.get_success_url())


class JardinEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 's5appadherant/jardin/edit.html'
    permission_required = 's5appadherant.change_jardin'
    form_class = JardinForm
    model = Jardin

    def get_success_url(self):
        return reverse('s5appadherant:jardin_detail', kwargs={
            'jardin_id': self.kwargs.get('pk')
        })

    def get_context_data(self, **kwargs):
        context = super(JardinEditView, self).get_context_data(**kwargs)
        context.update({
            'menu_actif': 'jardin',
            'titre_page': u"Édition d'un jardin : %s" % context.get('jardin').appelation
        })
        return context
