# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.views.generic import TemplateView

from s5appadherant.models import Adherant, Jardin, Cultivateur


class CultivateurConfirmationView(LoginRequiredMixin, TemplateView):
    template_name = 's5appadherant/cultivateur/confirmation.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'jardin_id': kwargs.get('jardin_id'),
            'titre_page': u"Demande prise en compte",
            'menu_actif': 'jardin'
        })


class CultivateurRequestView(LoginRequiredMixin, TemplateView):
    template_name = 's5appadherant/cultivateur/request.html'

    @staticmethod
    def _validate(jardin, adherant):
        if jardin.proprietaire == adherant:
            raise PermissionDenied("Vous proprietaire de ce jardin")

        qs = jardin.cultivateur_set.all()
        cultivateurs = [cultivateur.adherant for cultivateur in qs]

        if adherant in cultivateurs:
            acceptes = [cultivateur.adherant for cultivateur in qs.filter(accepte=True)]
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

        CultivateurRequestView._validate(jardin, adherant)

        return self.render_to_response({
            'jardin': jardin,
            'titre_page': u"Demande d'ajout comme cultivateur pour %s" % jardin.appelation,
            'menu_actif': 'jardin'
        })

    def post(self, request, *args, **kwargs):
        adherant = Adherant.objects.get_from_user(request.user)
        jardin_id = kwargs.get('jardin_id')

        try:
            jardin = Jardin.objects.get(pk=jardin_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("<h1>La page demandee n'existe pas</h1>")

        CultivateurRequestView._validate(jardin, adherant)

        cultivateur = Cultivateur()
        cultivateur.adherant = adherant
        cultivateur.jardin = jardin
        cultivateur.accepte = False
        cultivateur.save()

        return redirect(reverse('s5appadherant:cultivateur_confirmation', kwargs={
            'jardin_id': jardin_id
        }))