# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse, resolve
from django.template import Context
from django.template import Template
from s5vitrine.models import Menuitem


class MenuTest(TestCase):

    fixtures = ['base']

    def test_render(self):
        template = Template('{% load tags %}{% menu menu_actif %}')
        context = Context({})
        html = template.render(context)

        expected_html = """
            <nav class="navbar navbar-default">
                <div class="container">
                    <ul class="nav navbar-nav">
                        <li class="">
                            <a href="/">Accueil</a>
                        </li>
                        <li class="">
                            <a href="/contenus/1/">Contenu</a>
                        </li>
                        <li class="">
                            <a href="/contact/">Contact</a>
                        </li>
                    </ul>
                </div>
            </nav>"""
        self.assertHTMLEqual(expected_html, html)

    def test_render_with_active_menuitem(self):
        menuitem = Menuitem.objects.get(pk='accueil')

        template = Template('{% load tags %}{% menu menu_actif %}')
        context = Context({'menu_actif': menuitem})
        html = template.render(context)

        expected_html = """
            <nav class="navbar navbar-default">
                <div class="container">
                    <ul class="nav navbar-nav">
                        <li class="active">
                            <a href="/">Accueil</a>
                        </li>
                        <li class="">
                            <a href="/contenus/1/">Contenu</a>
                        </li>
                        <li class="">
                            <a href="/contact/">Contact</a>
                        </li>
                    </ul>
                </div>
            </nav>"""
        self.assertHTMLEqual(expected_html, html)


class AuthWidgetTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.factory = RequestFactory()

    def render_tag(self, request):
        template = Template('{% load tags %}{% auth_widget request %}')
        context = Context({
            'request': request
        })
        return template.render(context)

    def get_request(self, view_name, user):
        request = self.factory.get(view_name)
        request.user = user
        request.resolver_match = resolve(view_name)

        return request

    def test_render_connected(self):
        # La template doit contenir un lien deconnexion
        request = self.get_request(reverse('s5vitrine:accueil_view'), self.user)
        html = self.render_tag(request)

        logout_url = reverse('s5appadherant:logout_view')
        logout_link = u'<a href="%s" class="btn btn-xs btn-danger">Déconnexion</a>' % logout_url
        self.assertInHTML(logout_link, html)

    def test_render_not_connected(self):
        # La template doit contenir un lien connexion
        request = self.get_request(reverse('s5vitrine:accueil_view'), AnonymousUser())
        html = self.render_tag(request)

        login_url = reverse('s5appadherant:login_view')
        login_link = u'<a href="%s" class="btn btn-xs btn-primary">Connexion</a>' % login_url
        self.assertInHTML(login_link, html)

    def test_render_from_appadherant(self):
        # La template doit contenir un lien vers le site vitrine
        request = self.get_request(reverse('s5appadherant:accueil_view'), self.user)
        html = self.render_tag(request)

        vitrine_accueil_url = reverse('s5vitrine:accueil_view')
        vitrine_accueil_link = u'<a href="%s" class="btn btn-xs btn-primary">Retour au site</a>' % vitrine_accueil_url
        self.assertInHTML(vitrine_accueil_link, html)

    def test_render_from_vitrine(self):
        # Si l'user est connecté, la template doit contenir un lien vers l'appadherant
        request = self.get_request(reverse('s5vitrine:accueil_view'), self.user)
        html = self.render_tag(request)

        adherant_url = reverse('s5appadherant:accueil_view')
        adherant_link = u'<a href="%s" class="btn btn-xs btn-primary">Espace adhérant</a>' % adherant_url
        self.assertInHTML(adherant_link, html)
