# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from s5appadherant.models.variete import Variete
from s5vitrine.models.menuitem import Menuitem


class VarieteListView(TemplateView):

    template_name = 's5vitrine/variete_list.html'

    def get(self, request, *args, **kwargs):

        menuitem = Menuitem.objects.get(pk='variete_list')

        varietes_list = Variete.objects.all()
        paginator = Paginator(varietes_list, 12)
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


class VarieteDetailView(TemplateView):

    template_name = 's5vitrine/variete_detail.html'

    def get(self, request, *args, **kwargs):

        menuitem = Menuitem.objects.get(pk='variete_list')

        variete_id = kwargs.get('variete_id', None)
        try:
            variete = Variete.objects.get(pk=variete_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("<h1>La page demandee n'existe pas</h1>")

        return self.render_to_response({
            'variete': variete,
            'menu_actif': menuitem,
            'titre_page': u'Fiche variété : %s' % variete.nom
        })
