# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.views.generic import CreateView

from s5appadherant.forms.culture import CultureForm
from s5appadherant.models import Culture, Jardin


class HttpRedirectResponse(object):
    pass


class CultureAddView(LoginRequiredMixin, CreateView):
    template_name = 's5appadherant/culture/add.html'
    form_class = CultureForm
    model = Culture

    def get_jardin(self):
        jardin_id = self.kwargs.get('jardin_id')
        try:
            jardin = Jardin.objects.get(pk=jardin_id)
        except ObjectDoesNotExist:
            raise Http404
        return jardin

    def get_success_url(self):
        return reverse('s5appadherant:jardin_detail', kwargs={
            'jardin_id': self.kwargs.get('jardin_id')
        })

    def get_context_data(self, **kwargs):
        context = super(CultureAddView, self).get_context_data(**kwargs)
        context.update({
            'jardin': self.get_jardin(),
            'menu_actif': 'jardin',
            'titre_page': u"Ajout d'une variété cultivée"
        })
        return context

    def form_valid(self, form):
        culture = form.save(commit=False)
        culture.jardin = self.get_jardin()
        culture.save()
        return HttpResponseRedirect(self.get_success_url())

