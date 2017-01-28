from actstream.models import Action
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View


class ProcessActionView(LoginRequiredMixin, View):

    def get(self, request, **kwargs):
        action = get_object_or_404(Action, pk=kwargs.get('action_id'))
        request.user.adherant.processed_actions.add(action)
        request.user.adherant.save()

        return redirect('s5appadherant:accueil')
