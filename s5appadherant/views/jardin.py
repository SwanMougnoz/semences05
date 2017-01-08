# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import ListView, TemplateView
from django.views.generic import UpdateView

from s5appadherant.forms.jardin import JardinForm
from s5appadherant.models import Jardin, Adherant, Entretient
from s5appadherant.tables.culture import CultureTable


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

        culture_table = CultureTable(jardin=jardin)

        qs = jardin.entretient_set.all()
        cultivateurs_all = [entretient.adherant for entretient in qs]
        cultivateurs_acceptes = [entretient.adherant for entretient in qs.filter(accepte=True)]

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


class EntretientConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = 's5appadherant/jardin/entretient_confirmation.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'jardin_id': kwargs.get('jardin_id'),
            'titre_page': u"Demande prise en compte",
            'menu_actif': 'jardin'
        })


class JardinEntretientRequestView(LoginRequiredMixin, TemplateView):
    template_name = 's5appadherant/jardin/entretient_request.html'

    @staticmethod
    def _validate(jardin, adherant):
        if jardin.proprietaire == adherant:
            raise PermissionDenied("Vous proprietaire de ce jardin")

        qs = jardin.entretient_set.all()
        cultivateurs = [entretient.adherant for entretient in qs]

        if adherant in cultivateurs:
            acceptes = [entretient.adherant for entretient in qs.filter(accepte=True)]
            if adherant in acceptes:
                raise PermissionDenied("Vous cultivez déjà ce jardin")
            raise PermissionDenied("Vous avez déjà effectué une demande pour cultiver ce jardin. Celle-ci doit être accepté par le proprietaire")

    def get(self, request, *args, **kwargs):
        adherant = Adherant.objects.get_from_user(request.user)
        jardin_id = kwargs.get('jardin_id')

        try:
            jardin = Jardin.objects.get(pk=jardin_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("<h1>La page demandee n'existe pas</h1>")

        JardinEntretientRequestView._validate(jardin, adherant)

        return self.render_to_response({
            'jardin': jardin,
            'titre_page': u"Demande d'entretient pour %s" % jardin.appelation,
            'menu_actif': 'jardin'
        })

    def post(self, request, *args, **kwargs):
        adherant = Adherant.objects.get_from_user(request.user)
        jardin_id = kwargs.get('jardin_id')

        try:
            jardin = Jardin.objects.get(pk=jardin_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("<h1>La page demandee n'existe pas</h1>")

        JardinEntretientRequestView._validate(jardin, adherant)

        entretient = Entretient()
        entretient.adherant = adherant
        entretient.jardin = jardin
        entretient.accepte = False
        entretient.save()

        return redirect(reverse('s5appadherant:entretient_confirmation', kwargs={
            'jardin_id': jardin_id
        }))
