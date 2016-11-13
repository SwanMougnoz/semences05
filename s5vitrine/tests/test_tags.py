from django.test import TestCase
from django.template import Context
from django.template import Template
from s5vitrine.models import Menuitem


class MenuTest(TestCase):
    def setUp(self):
        home_menuitem = Menuitem()
        home_menuitem.identifier = 'home'
        home_menuitem.label = 'Accueil'
        home_menuitem.position = 1
        home_menuitem.save()

        contact_menuitem = Menuitem()
        contact_menuitem.identifier = 'contact'
        contact_menuitem.label = 'Contact'
        contact_menuitem.position = 2
        contact_menuitem.save()

    def test_render(self):
        template = Template('{% load tags %}{% menu menu_active %}')
        context = Context({})
        html = template.render(context)

        expected_html = """
            <nav class="navbar navbar-default">
                <div class="container">
                    <ul class="nav navbar-nav">
                        <li class="">
                            <a href="">Accueil</a>
                        </li>
                        <li class="">
                            <a href="">Contact</a>
                        </li>
                    </ul>
                </div>
            </nav>"""
        self.assertHTMLEqual(expected_html, html)

    def test_render_with_id(self):
        template = Template('{% load tags %}{% menu menu_active %}')
        context = Context({'menu_active': 'home'})
        html = template.render(context)

        expected_html = """
            <nav class="navbar navbar-default">
                <div class="container">
                    <ul class="nav navbar-nav">
                        <li class="active">
                            <a href="">Accueil</a>
                        </li>
                        <li class="">
                            <a href="">Contact</a>
                        </li>
                    </ul>
                </div>
            </nav>"""
        self.assertHTMLEqual(expected_html, html)
