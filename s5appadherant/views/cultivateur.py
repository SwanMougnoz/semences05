# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from rules.contrib.views import PermissionRequiredMixin

from s5appadherant.models import Jardin, Cultivateur
from s5appadherant.services.mailer import MailFactory
from s5appadherant import permissions


class CultivateurConfirmationView(LoginRequiredMixin, TemplateView):
    # todo: remplacer par un message en js (idem vitrine.contact ?)
    template_name = 's5appadherant/cultivateur/confirmation.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'jardin_id': kwargs.get('jardin_id'),
            'titre_page': u"Demande prise en compte",
            'menu_actif': 'jardin'
        })


class CultivateurRequestView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 's5appadherant/cultivateur/request.html'
    permission_required = 's5appadherant.add_cultivateur'

    def get_permission_object(self):
        return get_object_or_404(Jardin, pk=self.kwargs.get('jardin_id'))

    def get(self, request, *args, **kwargs):
        jardin = get_object_or_404(Jardin, pk=kwargs.get('jardin_id'))

        return self.render_to_response({
            'jardin': jardin,
            'titre_page': u"Demande d'ajout comme cultivateur pour %s" % jardin.appelation,
            'menu_actif': 'jardin'
        })

    def post(self, request, **kwargs):
        jardin = get_object_or_404(Jardin, pk=kwargs.get('jardin_id'))

        cultivateur = Cultivateur()
        cultivateur.adherant = request.user.adherant
        cultivateur.jardin = jardin
        cultivateur.accepte = False
        cultivateur.save()

        MailFactory.send('cultivateur_request', cultivateur=cultivateur)

        return redirect(reverse('s5appadherant:cultivateur_confirmation', kwargs={
            'jardin_id': jardin.id
        }))


class CultivateurDecideView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 's5appadherant/cultivateur/decide.html'
    permission_required = 's5appadherant.accept_cultivateur'

    def get_permission_object(self):
        return get_object_or_404(Cultivateur, pk=self.kwargs.get('cultivateur_id'))

    def get(self, request, *args, **kwargs):
        cultivateur = get_object_or_404(Cultivateur, pk=kwargs.get('cultivateur_id'))

        return self.render_to_response({
            'cultivateur': cultivateur,
            'titre_page': u"Ajout d'un cultivateur pour %s" % cultivateur.jardin.appelation,
            'menu_actif': 'jardin'
        })

    def post(self, request, **kwargs):
        cultivateur = get_object_or_404(Cultivateur, pk=kwargs.get('cultivateur_id'))

        if 'cultivateur_accept' in request.POST:
            cultivateur.accepte = True
            cultivateur.save()
            MailFactory.send('cultivateur_accept', cultivateur=cultivateur)
        elif 'cultivateur_deny' in request.POST:
            cultivateur.delete()
            MailFactory.send('cultivateur_deny', cultivateur=cultivateur)

        return redirect('s5appadherant:accueil')
