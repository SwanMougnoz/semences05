# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, AnonymousUser
from django.core.paginator import Paginator
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse, resolve
from django.template import Context
from django.template import Template
from s5vitrine.models import Menuitem
from s5appadherant.models.variete import Variete


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
                        <li class="">
                            <a href="/varietes/">Liste des variétés</a>
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
                        <li class="">
                            <a href="/varietes/">Liste des variétés</a>
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


class PaginationTest(TestCase):

    # 3 Variétés
    fixtures = ['varietes']

    def setUp(self):
        self.varietes = Variete.objects.all()

    def render_tag(self, page_length, page_number, queryset):
        paginator = Paginator(queryset, page_length)
        template = Template('{% load tags %}{% pagination page %}')
        page = paginator.page(page_number)
        context = Context({'page': page})
        return template.render(context)

    def test_require_page_object(self):
        # Le tag demande un objet de classe Page en paramètre,
        # ici on lui fourni un DataSet
        template = Template('{% load tags %}{% pagination not_a_page %}')
        context = Context({'not_a_page': self.varietes})

        with self.assertRaises(ValueError):
            template.render(context)

    def test_previous_page(self):
        # Test avec la première page, l'element doit être désactivé
        html = self.render_tag(page_length=2, page_number=1, queryset=self.varietes)
        no_previous_link = u'<li class="disabled"><span>Précédent</span></li>'
        self.assertInHTML(no_previous_link, html)

        # Test avec une autre page, l'élement doit contenir le bon lien
        html = self.render_tag(page_length=2, page_number=2, queryset=self.varietes)
        has_previous_link = u'<li><a href="?page=1"><span>Précédent</span></a></li>'
        self.assertInHTML(has_previous_link, html)

    def test_next_page(self):
        # Test avec la dernière page, l'element doit être désactivé
        html = self.render_tag(page_length=2, page_number=2, queryset=self.varietes)
        no_next_link = u'<li class="disabled"><span>Suivant</span></li>'
        self.assertInHTML(no_next_link, html)

        # Test avec une autre page, l'élement doit contenir le bon lien
        html = self.render_tag(page_length=2, page_number=1, queryset=self.varietes)
        has_next_link = u'<li><a href="?page=2"><span>Suivant</span></a></li>'
        self.assertInHTML(has_next_link, html)

    def test_page_numbers(self):
        html = self.render_tag(page_length=1, page_number=1, queryset=self.varietes)

        # L'élément vers page courante ne doit pas contenir de lien et avoir la classe 'active'
        current_element = u'<li class="active"><span>1<span class="sr-only">(current)</span></span></li>'
        self.assertInHTML(current_element, html)

        # Il doit y avoir au moins un lien vers toutes les autres page
        page2 = u'<li><a href="?page=2"><span>2</span></a></li>'
        page3 = u'<li><a href="?page=3"><span>3</span></a></li>'
        self.assertInHTML(page2, html)
        self.assertInHTML(page3, html)

