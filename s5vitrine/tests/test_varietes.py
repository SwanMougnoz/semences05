# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.paginator import Page
from s5vitrine.models.menuitem import Menuitem


class VarieteListTest(TestCase):

    fixtures = ['base']

    def test_get(self):
        response = self.client.get(reverse('s5vitrine:variete_list_view'))

        # La page doit retourner la bonne template
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('s5vitrine/variete_list.html')

        # L'item de menu doit correspondre à la liste des variétés
        self.assertIsInstance(response.context['menu_actif'], Menuitem)
        self.assertEqual('variete_list', response.context['menu_actif'].identifiant)

        # Le context doit contenir un queryset paginé
        self.assertIsInstance(response.context['varietes'], Page)
        self.assertEqual(1, response.context['varietes'].number)


class VarieteDetailTest(TestCase):

    fixtures = ['base', 'varietes']

    def test_get(self):
        response = self.client.get(reverse('s5vitrine:variete_detail_view', kwargs={
            'variete_id': 6
        }))

        # La page doit retourner la bonne template
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('s5vitrine/variete_detail.html')

        # L'item de menu doit correspondre à la liste des variétés
        self.assertIsInstance(response.context['menu_actif'], Menuitem)
        self.assertEqual('variete_list', response.context['menu_actif'].identifiant)

        # Si la variete n'existe pas, la réponse doit contenir une 404
        response = self.client.get(reverse('s5vitrine:variete_detail_view', kwargs={
            'variete_id': 46112
        }))

        self.assertEqual(404, response.status_code)
