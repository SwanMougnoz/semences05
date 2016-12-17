# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from s5appadherant.models import Jardin


class JardinListView(LoginRequiredMixin, ListView):
    template_name = 's5appadherant/jardin/list.html'
    model = Jardin

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        context = super(JardinListView, self).get_context_data(**kwargs)
        context.update({
            'menu_actif': 'jardin',
            'titre_page': u"Mes jardins"
        })
        return context
