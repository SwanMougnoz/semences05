# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from s5appadherant.models import Variete
from s5vitrine.models import Menuitem


class VarieteListView(TemplateView):

    template_name = 's5vitrine/variete_list.html'

    def get(self, request, *args, **kwargs):

        menuitem = Menuitem.objects.get(pk='variete_list')

        varietes_list = Variete.objects.all()
        paginator = Paginator(varietes_list, 3)
        page = request.GET.get('page')
        try:
            varietes = paginator.page(page)
        except PageNotAnInteger:
            varietes = paginator.page(1)
        except EmptyPage:
            varietes = paginator.page(paginator.num_pages)

        return self.render_to_response({
            'varietes': varietes,
            'menu_actif': menuitem,
            'titre_page': 'Toutes les variétés'
        })
