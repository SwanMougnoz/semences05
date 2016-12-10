# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.template import Context
from django.template import Template
from django.test import TestCase


class MenuAdherantTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def render_tag(self, context):
        template = Template('{% load tags_adherant %}{% menu_adherant user menu_actif %}')
        return template.render(Context(context))

    def test_guess_username(self):
        # Test avec un user dont les nom+prenom ne sont pas renseignés
        html = self.render_tag({
            'user': self.user,
            'menu_actif': None
        })
        self.assertInHTML(u'<a href="/adherant/" class="list-group-item "><i class="fa fa-home"></i>Accueil</a>', html)

        # Test avec un user dont les nom+prenom sont renseignés
        self.user.first_name = 'John'
        self.user.last_name = 'Lennon'

        html = self.render_tag({
            'user': self.user,
            'menu_actif': None
        })
        self.assertInHTML(u'<a href="/adherant/" class="list-group-item "><i class="fa fa-home"></i>John Lennon</a>', html)

    def test_has_active(self):
        html = self.render_tag({
            'user': self.user,
            'menu_actif': 'accueil'
        })
        self.assertIn('active', html)
