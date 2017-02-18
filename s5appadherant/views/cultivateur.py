# -*- coding: utf-8 -*-
import logging
from actstream import action
from actstream.actions import follow, unfollow
from actstream.models import Action
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import View
from rules.contrib.views import PermissionRequiredMixin

from s5appadherant.models import Jardin, Cultivateur
from s5mailing.views.cultivateur import CultivateurRequestMessageView, CultivateurAcceptMessageView, \
    CultivateurDenyMessageView, CultivateurDeleteMessageView, CultivateurQuitMessageView
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
    permission_required = 's5appadherant.request_cultivateur'

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
        cultivateur.save()

        # Création d'une action pour la demande d'ajout et suivi de celle-ci par les deux parties
        action.send(request.user, verb="request", action_object=cultivateur)
        follow(request.user, cultivateur, actor_only=False, send_action=False)
        follow(jardin.proprietaire.user, cultivateur, actor_only=False, send_action=False)

        CultivateurRequestMessageView(cultivateur, request).send()

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
            cultivateur.accept()

            # Création d'une action pour l'acceptation et ajout de l'adherant dans les followers du jardin
            action.send(request.user, verb="accept", action_object=cultivateur)
            follow(cultivateur.adherant.user, cultivateur.jardin, actor_only=False, send_action=False)

            CultivateurAcceptMessageView(cultivateur, request).send()

        elif 'cultivateur_deny' in request.POST:
            cultivateur.deny()
            action.send(request.user, verb="deny", action_object=cultivateur)
            CultivateurDenyMessageView(cultivateur, request).send()

        try:
            request_action = Action.objects.get_by_terms('request', cultivateur)
            request.user.adherant.processed_actions.add(request_action)
            request.user.adherant.save()
        except ObjectDoesNotExist:
            logging.warning("CultivateurDecide : Action request manquante (Cultivateur id : %d)" % cultivateur.id)

        return redirect('s5appadherant:accueil')


class CultivateurQuitView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        jardin = get_object_or_404(Jardin, pk=self.kwargs.get('jardin_id'))
        cultivateur = get_object_or_404(Cultivateur, pk=self.kwargs.get('cultivateur_id'))

        if cultivateur.jardin != jardin:
            return HttpResponseForbidden()

        if cultivateur.adherant.user != request.user:
            return HttpResponseForbidden()

        if cultivateur.pending or not cultivateur.accepte:
            return HttpResponseForbidden()

        cultivateur.accepte = False
        cultivateur.save()

        action.send(request.user, verb='quit', action_object=cultivateur)
        unfollow(cultivateur.adherant.user, jardin)

        CultivateurQuitMessageView(cultivateur, request).send()

        return redirect('s5appadherant:jardin_detail', jardin_id=jardin.id)


class CultivateurDeleteView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 's5appadherant.manage_cultivateurs'

    def get_permission_object(self):
        return get_object_or_404(Jardin, pk=self.kwargs.get('jardin_id'))

    def get(self, request, *args, **kwargs):
        jardin = get_object_or_404(Jardin, pk=kwargs.get('jardin_id'))
        cultivateur = get_object_or_404(Cultivateur, pk=kwargs.get('cultivateur_id'))

        if cultivateur.jardin != jardin:
            return HttpResponseForbidden()

        if cultivateur.pending or not cultivateur.accepte:
            return HttpResponseForbidden()

        cultivateur.accepte = False
        cultivateur.save()

        action.send(request.user, verb='delete', action_object=cultivateur)
        unfollow(cultivateur.adherant.user, jardin)

        CultivateurDeleteMessageView(cultivateur, request).send()

        return redirect('s5appadherant:jardin_detail', jardin_id=jardin.id)
