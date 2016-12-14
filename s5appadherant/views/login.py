# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth import authenticate, login, logout
from s5appadherant.forms.login import LoginForm


class LoginView(TemplateView):

    template_name = "s5appadherant/login.html"

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated():
            return redirect("s5appadherant:accueil")
        else:
            form = kwargs.get('form', LoginForm())
            return self.render_to_response({
                'form': form,
                'titre_page': 'Connexion - Espace adhérant'
            })

    def post(self, request):

        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("s5appadherant:accueil")

        return self.render_to_response({
            'form': form,
            'on_error': True,
            'message': "L'email ou le mot de passe est incorrect",
            'titre_page': 'Connexion - Espace adhérant'
        })


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
