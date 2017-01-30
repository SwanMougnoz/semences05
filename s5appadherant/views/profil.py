# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from table.views import FeedDataView

from s5appadherant.forms.adresse import AdresseForm
from s5appadherant.forms.adherant import UserForm, AdherantForm
from s5appadherant.models import Adherant, Jardin
from s5appadherant.tables.jardin import ProfilJardinTable


class ProfilDetailView(LoginRequiredMixin, TemplateView):
    template_name = 's5appadherant/profil/detail.html'

    def get(self, request, *args, **kwargs):
        adherant_id = kwargs.get('adherant_id')

        if adherant_id is None:
            adherant = request.user.adherant
        else:
            adherant = get_object_or_404(Adherant, pk=adherant_id)

        jardin_table = ProfilJardinTable(adherant=adherant)

        return self.render_to_response({
            'adherant': adherant,
            'jardin_table': jardin_table,
            'menu_actif': 'profil',
            'titre_page': 'Profil'
        })


class ProfilEditView(LoginRequiredMixin, TemplateView):
    template_name = 's5appadherant/profil/edit.html'

    def get(self, request, *args, **kwargs):
        adherant = request.user.adherant

        user_form = UserForm(prefix='user', instance=request.user)
        adherant_form = AdherantForm(prefix='adherant', instance=adherant)
        adresse_form = AdresseForm(prefix='adresse', instance=adherant.adresse)

        return self.render_to_response({
            'user_form': user_form,
            'adherant_form': adherant_form,
            'adresse_form': adresse_form,
            'menu_actif': 'profil',
            'titre_page': u'Éditer mon profil'
        })

    def post(self, request):
        adherant = request.user.adherant

        user_form = UserForm(request.POST, prefix='user', instance=request.user)
        adherant_form = AdherantForm(request.POST, prefix='adherant', instance=adherant)
        adresse_form = AdresseForm(request.POST, prefix='adresse', instance=adherant.adresse)

        if user_form.is_valid() * adherant_form.is_valid() * adresse_form.is_valid():
            user = user_form.save()
            adresse = adresse_form.save()
            adherant = adherant_form.save(commit=False)
            adherant.user = user
            adherant.adresse = adresse
            adherant.save()

            return redirect('s5appadherant:profil_current')

        return self.render_to_response({
            'user_form': user_form,
            'adherant_form': adherant_form,
            'adresse_form': adresse_form,
            'menu_actif': 'profil',
            'titre_page': u'Éditer mon profil'
        })


class ProfilJardinDataView(FeedDataView):
    token = ProfilJardinTable.token

    def get_queryset(self):
        adherant_id = self.kwargs.get('adherant_id')
        return Jardin.objects.filter(
            Q(proprietaire_id=adherant_id)
            | (Q(cultivateur__adherant_id=adherant_id) & Q(cultivateur__accepte=True))
        ).distinct()
