# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

from s5appadherant.forms.adherant import UserForm, AdherantForm
from s5appadherant.models import Adherant


class ProfilDetailView(LoginRequiredMixin, TemplateView):
    template_name = 's5appadherant/profil/detail.html'

    def get(self, request, *args, **kwargs):
        adherant = Adherant.objects.get_from_user(request.user)

        return self.render_to_response({
            'adherant': adherant,
            'menu_actif': 'profil',
            'titre_page': 'Profil'
        })


class ProfilEditView(LoginRequiredMixin, TemplateView):
    template_name = 's5appadherant/profil/edit.html'

    def get(self, request, *args, **kwargs):
        adherant = Adherant.objects.get_from_user(request.user)

        user_form = UserForm(prefix='user', instance=request.user)
        adherant_form = AdherantForm(prefix='adherant', instance=adherant)

        return self.render_to_response({
            'user_form': user_form,
            'adherant_form': adherant_form,
            'menu_actif': 'profil',
            'titre_page': u'Éditer mon profil'
        })

    def post(self, request):
        adherant = Adherant.objects.get_from_user(request.user)

        user_form = UserForm(request.POST, prefix='user', instance=request.user)
        adherant_form = AdherantForm(request.POST, prefix='adherant', instance=adherant)

        if user_form.is_valid() * adherant_form.is_valid():
            user = user_form.save()
            adherant = adherant_form.save(commit=False)
            adherant.user = user
            adherant.save()

            return redirect('s5appadherant:profil_detail')

        return self.render_to_response({
            'user_form': user_form,
            'adherant_form': adherant_form,
            'menu_actif': 'profil',
            'titre_page': u'Éditer mon profil'
        })
