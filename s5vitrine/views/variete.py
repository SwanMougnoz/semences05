# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from s5appadherant.models import Variete
from s5vitrine.models import Menuitem


class VarieteListView(TemplateView):

    template_name = 's5vitrine/variete_list.html'

    def get(self, request, *args, **kwargs):

        varietes = Variete.objects.all()
        menuitem = Menuitem.objects.get(pk='variete_list')

        return self.render_to_response({
            'varietes': varietes,
            'menu_actif': menuitem,
            'titre_page': 'Toutes les variétés'
        })
