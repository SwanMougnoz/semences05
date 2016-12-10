# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from s5appadherant.models import Variete


class VarietelistView(TemplateView):

    template_name = 's5appadherant/variete_list.html'

    def get(self, request, *args, **kwargs):

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
            'titre_page': 'Toutes les variétés',
            'menu_actif': 'variete'
        })


class VarieteDetailView(TemplateView):

    template_name = 's5appadherant/variete_detail.html'

    def get(self, request, *args, **kwargs):

        variete_id = kwargs.get('variete_id', None)
        try:
            variete = Variete.objects.get(pk=variete_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("<h1>La page demandee n'existe pas</h1>")

        return self.render_to_response({
            'variete': variete,
            'menu_actif': 'variete',
            'titre_page': u'Fiche variété : %s' % variete.nom
        })
