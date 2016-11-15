from django.test import TestCase
from s5vitrine.models import Menuitem


class HomeTest(TestCase):

    fixtures = ['base']

    def test_get(self):
        response = self.client.get('/')

        # La page doit retourner la bonne template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 's5vitrine/home.html')

        # L'item de menu doit correspondre au menu principal
        self.assertIsInstance(response.context['menu_active'], Menuitem)
        self.assertEqual('home', response.context['menu_active'].identifier)
