# -*- coding: utf-8 -*-
from django.test import TestCase
from s5vitrine.forms.contact import ContactForm
from s5vitrine.models.menuitem import Menuitem


class ContactTest(TestCase):

    fixtures = ['base']

    def test_get(self):
        response = self.client.get('/contact/')

        # La page doit retourner la bonne template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 's5vitrine/contact/form.html')

        # L'item de menu doit correspondre au menu principal
        self.assertIsInstance(response.context['menu_actif'], Menuitem)
        self.assertEqual('contact', response.context['menu_actif'].identifiant)

        # Le context doit contenir le formulaire approprié
        self.assertIsInstance(response.context['form'], ContactForm)

