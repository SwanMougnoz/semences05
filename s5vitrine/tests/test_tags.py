from django.test import TestCase
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
