# -*- coding: utf-8 -*-
from django.views.generic import TemplateView


class AccueilView(TemplateView):

    template_name = 's5appadherant/accueil.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
