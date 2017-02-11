# -*- coding: utf-8 -*-
import datetime
from django.core.urlresolvers import reverse, resolve
from django.http import Http404
from django.test import RequestFactory
from django.test import TestCase
from django_dynamic_fixture import G
from with_asserts.mixin import AssertHTMLMixin

from s5appadherant.forms.culture import CultureForm
from s5appadherant.models import Adherant, Variete, Culture, User, Jardin, Cultivateur
from s5appadherant.views.culture import CultureAddView, CultureDeleteView


class CultureAddTest(TestCase, AssertHTMLMixin):

    def setUp(self):
        self.factory = RequestFactory()
        self.adherant = G(Adherant, user=G(User))
        self.jardin = G(Jardin, proprietaire=self.adherant)
        [G(Variete) for i in range(1, 5)]

    def request(self, jardin, method='get', data=None):
        params = {'jardin_id': jardin.id}
        url = reverse('s5appadherant:culture_new', kwargs=params)

        if method == 'get':
            request = self.factory.get(url)
        else:
            request = self.factory.post(url, data=data)

        request.user = self.adherant.user
        request.resolver_match = resolve(url)

        return CultureAddView.as_view()(request, **params)

    def test_get(self):
        response = self.request(self.jardin)

        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.context_data['form'], CultureForm)

        # Le document doit contenir les champs de formulaire appropriés
        response.render()

        with self.assertHTML(response, 'select[name="variete"] option') as options:
            variete_count = Variete.objects.all().count()
            self.assertEqual(variete_count + 1, len(options))  # + 1 pour le champ vide

        with self.assertHTML(response, 'input[name="variete_nom"]'):
            pass
        with self.assertHTML(response, 'textarea[name="variete_description"]'):
            pass
        with self.assertHTML(response, 'select[name="type_conservation"]'):
            pass
        with self.assertHTML(response, 'input[name="variete_photo"]'):
            pass

    def test_post_select_variete(self):
        variete = Variete.objects.first()
        today = datetime.date.today()
        post_data = {
            'date_debut': today,
            'variete': variete.id,
            'type_conservation': 'dynamique'
        }

        pre_add_culture_count = Culture.objects.filter(jardin=self.jardin).count()
        pre_add_variete_count = Variete.objects.all().count()

        self.request(self.jardin, 'post', post_data)

        post_add_culture_count = Culture.objects.filter(jardin=self.jardin).count()
        post_add_variete_count = Variete.objects.all().count()

        self.assertEqual((pre_add_culture_count + 1), post_add_culture_count)
        self.assertEqual(pre_add_variete_count, post_add_variete_count)

        culture = self.jardin.culture_set.first()
        self.assertEqual(today, culture.date_debut)
        self.assertEqual('dynamique', culture.type_conservation)
        self.assertEqual(variete, culture.variete)
        self.assertIsNone(culture.date_fin)
        self.assertIsNotNone(culture.date_debut)

    def test_post_new_variete(self):
        today = datetime.date.today()
        post_data = {
            'date_debut': today,
            'variete_nom': 'Nouvelle variété !',
            'variete_description': 'Bla bla bla',
            'type_conservation': 'conservatoire'
        }

        pre_add_culture_count = Culture.objects.filter(jardin=self.jardin).count()
        pre_add_variete_count = Variete.objects.all().count()

        self.request(self.jardin, 'post', post_data)

        post_add_culture_count = Culture.objects.filter(jardin=self.jardin).count()
        post_add_variete_count = Variete.objects.all().count()

        self.assertEqual((pre_add_culture_count + 1), post_add_culture_count)
        self.assertEqual((pre_add_variete_count + 1), post_add_variete_count)

        culture = self.jardin.culture_set.first()
        self.assertEqual(today, culture.date_debut)
        self.assertEqual('conservatoire', culture.type_conservation)
        self.assertEqual(u'Nouvelle variété !', culture.variete.nom)
        self.assertEqual('Bla bla bla', culture.variete.description)
        self.assertIsNone(culture.date_fin)
        self.assertIsNotNone(culture.date_debut)

    def test_post_no_variete(self):
        post_data = {
            'variete': '',
            'type_conservation': 'conservatoire'
        }

        pre_add_culture_count = Culture.objects.filter(jardin=self.jardin).count()
        pre_add_variete_count = Variete.objects.all().count()

        self.request(self.jardin, 'post', post_data)

        post_add_culture_count = Culture.objects.filter(jardin=self.jardin).count()
        post_add_variete_count = Variete.objects.all().count()

        self.assertEqual(pre_add_culture_count, post_add_culture_count)
        self.assertEqual(pre_add_variete_count, post_add_variete_count)


class CultureDeleteTest(TestCase):
    def setUp(self):
        self.proprietaire = G(Adherant)
        self.jardin = G(Jardin, proprietaire=self.proprietaire)
        self.variete = G(Variete)
        self.culture = G(Culture, jardin=self.jardin, variete=self.variete, date_fin=None)

        self.factory = RequestFactory()

    def _get(self, jardin_id, culture_id, user):
        params = {
            'jardin_id': jardin_id,
            'culture_id': culture_id
        }
        request = self.factory.get(reverse('s5appadherant:culture_delete', kwargs=params))
        request.user = user

        return CultureDeleteView.as_view()(request, **params)

    def test_get(self):
        response = self._get(self.jardin.id, self.culture.id, self.proprietaire.user)
        self.assertEqual(302, response.status_code)

        culture_loaded = Culture.objects.get(pk=self.culture.id)
        self.assertIsNotNone(culture_loaded.date_fin)

    def test_get_already_deleted(self):
        self.culture.date_fin = datetime.date.today()
        self.culture.save()

        response = self._get(self.jardin.id, self.culture.id, self.proprietaire.user)
        self.assertEqual(403, response.status_code)

        # L'objet ne doit pas avoir changé
        culture_loaded = Culture.objects.get(pk=self.culture.id)
        self.assertEqual(self.culture, culture_loaded)

    def test_get_culture_inexistant(self):
        with self.assertRaises(Http404):
            self._get(self.jardin.id, 666, self.proprietaire.user)

    def test_get_culture_jardin_doesnt_match(self):
        new_jardin = G(Jardin, proprietaire=self.proprietaire)

        response = self._get(new_jardin.id, self.culture.id, self.proprietaire.user)
        self.assertEqual(403, response.status_code)

        # L'objet ne doit pas avoir changé
        culture_loaded = Culture.objects.get(pk=self.culture.id)
        self.assertEqual(self.culture, culture_loaded)

    def test_get_cultivateur(self):
        adherant = G(Adherant)
        G(Cultivateur, jardin=self.jardin, adherant=adherant, accepte=True, pending=False)

        response = self._get(self.jardin.id, self.culture.id, adherant.user)
        self.assertEqual(302, response.status_code)

        culture_loaded = Culture.objects.get(pk=self.culture.id)
        self.assertIsNotNone(culture_loaded.date_fin)

    def test_get_guest(self):
        adherant = G(Adherant)

        response = self._get(self.jardin.id, self.culture.id, adherant.user)
        self.assertEqual(302, response.status_code)

        # L'objet ne doit pas avoir changé
        culture_loaded = Culture.objects.get(pk=self.culture.id)
        self.assertEqual(self.culture, culture_loaded)

