# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.views.generic import ListView, TemplateView
from django.views.generic import UpdateView

from s5appadherant.forms.jardin import JardinForm
from s5appadherant.models import Jardin, Adherant


class JardinListView(LoginRequiredMixin, ListView):
    template_name = 's5appadherant/jardin/list.html'
    model = Jardin
    paginate_by = 10

    def get_queryset(self):
        adherant = Adherant.objects.get_from_user(self.request.user)
        return Jardin.objects.filter(proprietaire=adherant)

    def get_context_data(self, **kwargs):
        context = super(JardinListView, self).get_context_data(**kwargs)
        context.update({
            'jardins': context.get('page_obj'),
            'menu_actif': 'jardin',
            'titre_page': u"Mes jardins"
        })
        return context


class JardinDetailView(LoginRequiredMixin, TemplateView):
    template_name = 's5appadherant/jardin/detail.html'

    def get(self, request, *args, **kwargs):
        jardin_id = kwargs.get('jardin_id', None)
        try:
            jardin = Jardin.objects.get(pk=jardin_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("<h1>La page demandee n'existe pas</h1>")

        adherant = Adherant.objects.get_from_user(request.user)
        if jardin.proprietaire != adherant:
            return HttpResponseForbidden()

        return self.render_to_response({
            'jardin': jardin,
            'menu_actif': 'jardin',
            'titre_page': u'Jardin - %s' % jardin.appelation
        })


class JardinAddView(LoginRequiredMixin, CreateView):
    template_name = 's5appadherant/jardin/edit.html'
    form_class = JardinForm
    model = Jardin

    def get_success_url(self):
        return reverse('s5appadherant:jardin_list')

    def get_context_data(self, **kwargs):
        context = super(JardinAddView, self).get_context_data(**kwargs)
        context.update({
            'menu_actif': 'jardin',
            'titre_page': u"Ajout d'un jardin"
        })
        return context

    def form_valid(self, form):
        adherant = Adherant.objects.get_from_user(self.request.user)
        jardin = form.save(commit=False)
        jardin.proprietaire = adherant
        jardin.save()

        return HttpResponseRedirect(self.get_success_url())


class JardinEditView(LoginRequiredMixin, UpdateView):
    template_name = 's5appadherant/jardin/edit.html'
    form_class = JardinForm
    model = Jardin

    def get_success_url(self):
        return reverse('s5appadherant:jardin_list')

    def get_context_data(self, **kwargs):
        context = super(JardinEditView, self).get_context_data(**kwargs)
        context.update({
            'menu_actif': 'jardin',
            'titre_page': u"Édition d'un jardin : %s" % context.get('jardin').appelation
        })
        return context

    def form_valid(self, form):
        adherant = Adherant.objects.get_from_user(self.request.user)
        jardin = form.save(commit=False)
        jardin.proprietaire = adherant
        jardin.save()

        return HttpResponseRedirect(self.get_success_url())