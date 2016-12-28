# -*- coding: utf-8 -*-
from django.test import TestCase
from django.conf import settings
from s5vitrine.models.menuitem import Menuitem


class AccueilTest(TestCase):

    fixtures = ['base']

    # On s'assure que compress n'est pas activé pour tester la bonne inclusion des js
    def __init__(self, methodName):
        super(AccueilTest, self).__init__(methodName)
        self.original_compress_enabled = settings.COMPRESS_ENABLED

    def setUp(self):
        settings.COMPRESS_ENABLED = False

    def tearDown(self):
        settings.COMPRESS_ENABLED = self.original_compress_enabled

    def test_get(self):
        response = self.client.get('/')

        # La page doit retourner la bonne template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 's5vitrine/accueil.html')

        # L'item de menu doit correspondre au menu principal
        self.assertIsInstance(response.context['menu_actif'], Menuitem)
        self.assertEqual('accueil', response.context['menu_actif'].identifiant)

        # La page doit contenir un element pour la carte et avoir chargé les ressources leaflet
        self.assertContains(response, '<div id="vitrine-map"></div>')
        self.assertContains(response, '<script type="text/javascript" src="/static/jquery/dist/jquery.min.js"></script>')
        self.assertContains(response, '<script type="text/javascript" src="/static/leaflet/dist/leaflet.js"></script>')
        self.assertContains(response, '<script type="text/javascript" src="/static/s5vitrine/js/map.js"></script>')
