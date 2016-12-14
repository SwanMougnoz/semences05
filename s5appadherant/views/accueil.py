# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class AccueilView(LoginRequiredMixin, TemplateView):

    template_name = 's5appadherant/accueil.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'menu_actif': 'accueil'
        })
