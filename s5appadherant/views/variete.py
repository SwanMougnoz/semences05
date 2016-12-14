# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView
from s5appadherant.models.variete import Variete
from s5appadherant.forms.variete import VarieteForm


class VarieteListView(LoginRequiredMixin, TemplateView):

    template_name = 's5appadherant/variete_list.html'

    def get(self, request, *args, **kwargs):

        varietes_list = Variete.objects.all()
        paginator = Paginator(varietes_list, 10)
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


class VarieteDetailView(LoginRequiredMixin, TemplateView):

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


class VarieteAddView(LoginRequiredMixin, CreateView):
    template_name = 's5appadherant/variete_edit.html'
    form_class = VarieteForm
    model = Variete

    def get_success_url(self):
        return reverse('s5appadherant:variete_list')

    def get_context_data(self, **kwargs):
        context = super(VarieteAddView, self).get_context_data(**kwargs)
        context.update({
            'menu_actif': 'variete',
            'titre_page': u"Ajout d'une variété"
        })
        return context


class VarieteEditView(LoginRequiredMixin, UpdateView):
    template_name = 's5appadherant/variete_edit.html'
    form_class = VarieteForm
    model = Variete

    def get_success_url(self):
        return reverse('s5appadherant:variete_list')

    def get_context_data(self, **kwargs):
        context = super(VarieteEditView, self).get_context_data(**kwargs)
        context.update({
            'menu_actif': 'variete',
            'titre_page': u"Édition d'une variété"
        })
        return context
