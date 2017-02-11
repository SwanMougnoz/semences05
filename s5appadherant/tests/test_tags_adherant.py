# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.template import Context
from django.template import Template
from django.test import RequestFactory
from django.test import TestCase
from django_dynamic_fixture import G

from s5appadherant.models import Adherant


class MenuAdherantTest(TestCase):

    def setUp(self):
        self.adherant = G(Adherant, user__first_name='', user__last_name='')
        self.factory = RequestFactory()

    @staticmethod
    def render_tag(context):
        template = Template('{% load tags_adherant %}{% menu_adherant request menu_actif %}')
        return template.render(Context(context))

    def test_guess_username(self):
        request = self.factory.get(reverse('s5appadherant:accueil'))
        request.user = self.adherant.user

        # Test avec un user dont les nom+prenom ne sont pas renseignés
        html = self.render_tag({
            'request': request,
            'menu_actif': None
        })
        self.assertInHTML(u'<a href="/adherant/" class="list-group-item "><i class="fa fa-home"></i>Accueil</a>', html)

        # Test avec un user dont les nom+prenom sont renseignés
        self.adherant.user.first_name = 'John'
        self.adherant.user.last_name = 'Lennon'
        self.adherant.user.save()

        html = self.render_tag({
            'request': request,
            'menu_actif': None
        })
        self.assertInHTML(u'<a href="/adherant/" class="list-group-item "><i class="fa fa-home"></i>John Lennon</a>', html)

    def test_has_active(self):
        request = self.factory.get(reverse('s5appadherant:accueil'))
        request.user = self.adherant.user

        html = self.render_tag({
            'request': request,
            'menu_actif': 'accueil'
        })
        self.assertIn('active', html)
