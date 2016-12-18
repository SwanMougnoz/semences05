# -*- coding: utf-8 -*-
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Page
from django.core.urlresolvers import reverse, resolve
from django.test import RequestFactory
from django.test import TestCase
from with_asserts.mixin import AssertHTMLMixin

from s5appadherant.forms.jardin import JardinForm
from s5appadherant.models import Adherant, Jardin
from s5appadherant.views.jardin import JardinListView, JardinDetailView, JardinAddView, JardinEditView


class JardinListTest(TestCase, AssertHTMLMixin):

    fixtures = ['jardin']

    def setUp(self):
        self.factory = RequestFactory()
        self.adherant = Adherant.objects.get(pk=1)

    def test_get(self):
        url = reverse('s5appadherant:jardin_list')

        request = self.factory.get(url)
        request.user = self.adherant.user
        request.resolver_match = resolve(url)
        response = JardinListView.as_view()(request)

        self.assertEqual(200, response.status_code)

        # Le context doit contenir un queryset paginé
        self.assertIsInstance(response.context_data['jardins'], Page)
        self.assertEqual(1, response.context_data['jardins'].number)

        jardins = Jardin.objects.filter(proprietaire=self.adherant)
        jardin_count = len(jardins)

        response.render()

        # Tous les jardins et uniquement les jardins de l'adherant doivent être sur la page
        # et contenir un lien vers leur détail
        with self.assertHTML(response, '.jardin-list li') as (elems):
            self.assertEqual(jardin_count, len(elems))

        for jardin in jardins:
            detail_url = reverse('s5appadherant:jardin_detail', kwargs={
                'jardin_id': jardin.id
            })
            with self.assertHTML(response, 'a[href="%s"]' % detail_url) as (elem,):
                pass

        # Un lien vers la page d'ajout d'un jardin doit être présent
        add_url = reverse('s5appadherant:jardin_new')
        with self.assertHTML(response, 'a[href="%s"]' % add_url) as (elem,):
            pass

    def test_get_login_required(self):
        request = self.factory.get(reverse('s5appadherant:variete_list'))
        request.user = AnonymousUser()
        response = JardinListView.as_view()(request)

        # La page ne doit pas être accessible
        self.assertEqual(302, response.status_code)


class JardinDetailTest(TestCase, AssertHTMLMixin):

    fixtures = ['jardin']

    def setUp(self):
        self.factory = RequestFactory()
        self.adherant = Adherant.objects.get(pk=1)

    def test_get(self):
        jardin = self.adherant.jardin_set.first()
        params = {'jardin_id': jardin.id}
        url = reverse('s5appadherant:jardin_detail', kwargs=params)

        request = self.factory.get(url)
        request.user = self.adherant.user
        request.resolver_match = resolve(url)
        response = JardinDetailView.as_view()(request, **params)

        self.assertEqual(200, response.status_code)

        response.render()

        # Le document doit contenir toutes les informations relative au jardin
        self.assertContains(response, jardin.adresse.commune)
        self.assertContains(response, jardin.adresse.altitude)
        self.assertContains(response, jardin.appelation)
        self.assertContains(response, jardin.exposition)
        self.assertContains(response, jardin.type_sol)
        self.assertContains(response, '%s m²' % str(jardin.superficie).replace('.', ','))
        self.assertContains(response, jardin.irrigation)
        self.assertContains(response, jardin.mise_en_culture)
        # self.assertContains(response, jardin.description)

        # Le document doit contenir un lien vers la page d'édition de ce jardin
        edit_url = reverse('s5appadherant:jardin_edit', kwargs={
            'pk': jardin.id
        })
        with self.assertHTML(response, 'a[href="%s"]' % edit_url) as (elem,):
            pass


class JardinAddTest(TestCase, AssertHTMLMixin):

    fixtures = ['jardin']

    def setUp(self):
        self.factory = RequestFactory()
        self.adherant = Adherant.objects.get(pk=1)

    def test_get(self):
        url = reverse('s5appadherant:jardin_new')

        request = self.factory.get(url)
        request.user = self.adherant.user
        request.resolver_match = resolve(url)
        response = JardinAddView.as_view()(request)

        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.context_data['form'], JardinForm)

        response.render()

        # Le document doit contenir tous les champs de JardinForm
        expected_inputs = (
            'appelation',
            'exposition',
            'type_sol',
            'irrigation',
            'mise_en_culture',
            'superficie',
            'adresse',
            'commune',
            'latitude',
            'longitude',
            'altitude'
        )
        for input_elem in expected_inputs:
            with self.assertHTML(response, 'input[name="%s"]' % input_elem) as (elem,):
                pass
        with self.assertHTML(response, 'textarea[name="description"]') as (elem,):
            pass

        with self.assertHTML(response, '*[type="submit"]') as (elem,):
            pass

    def test_post(self):
        count = Jardin.objects.filter(proprietaire=self.adherant).count()
        url = reverse('s5appadherant:jardin_new')
        post_data = {
            'appelation': 'Nouveau jardin',
            'description': 'Bla bla bla',
            'exposition': '123',
            'type_sol': 'Sableux',
            'irrigation': 'Arrosoir',
            'mise_en_culture': '2014',
            'superficie': '150.0',
            'adresse': 'Au coin de la rue',
            'commune': 'Voiron',
            'latitude': '54.61353',
            'longitude': '45.38131',
            'altitude': '453'
        }

        request = self.factory.post(url, data=post_data)
        request.user = self.adherant.user
        request.resolver_match = resolve(url)
        JardinAddView.as_view()(request)

        post_add_count = Jardin.objects.filter(proprietaire=self.adherant).count()
        jardin = Jardin.objects.all().order_by('-id')[0]

        self.assertEqual(count + 1, post_add_count)
        self.assertEqual('Nouveau jardin', jardin.appelation)
        self.assertEqual('Bla bla bla', jardin.description)
        self.assertEqual(123, jardin.exposition)
        self.assertEqual('Sableux', jardin.type_sol)
        self.assertEqual('Arrosoir', jardin.irrigation)
        self.assertEqual(2014, jardin.mise_en_culture)
        self.assertEqual(150.0, jardin.superficie)
        self.assertEqual('Au coin de la rue', jardin.adresse.adresse)
        self.assertEqual('Voiron', jardin.adresse.commune)
        self.assertEqual(54.61353, jardin.adresse.latitude)
        self.assertEqual(45.38131, jardin.adresse.longitude)
        self.assertEqual(453, jardin.adresse.altitude)


class JardinEditTest(TestCase, AssertHTMLMixin):

    fixtures = ['jardin']

    def setUp(self):
        self.factory = RequestFactory()
        self.adherant = Adherant.objects.get(pk=1)

    def test_get(self):
        jardin = self.adherant.jardin_set.first()
        params = {'pk': jardin.id}
        url = reverse('s5appadherant:jardin_edit', kwargs=params)

        request = self.factory.get(url)
        request.user = self.adherant.user
        request.resolver_match = resolve(url)
        response = JardinEditView.as_view()(request, **params)

        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.context_data['form'], JardinForm)

        response.render()

        # Le document doit contenir tous les champs de JardinForm
        expected_inputs = {
            'appelation': jardin.appelation,
            'exposition': jardin.exposition,
            'type_sol': jardin.type_sol,
            'irrigation': jardin.irrigation,
            'mise_en_culture': jardin.mise_en_culture,
            'superficie': jardin.superficie,
            'adresse': jardin.adresse.adresse,
            'commune': jardin.adresse.commune,
            'latitude': jardin.adresse.latitude,
            'longitude': jardin.adresse.longitude,
            'altitude': jardin.adresse.altitude
        }
        for input_elem, expected_value in expected_inputs.items():
            with self.assertHTML(response, 'input[name="%s"]' % input_elem) as (elem,):
                if expected_value is not None:
                    expected_value = str(expected_value)
                self.assertEqual(expected_value, elem.value)
        with self.assertHTML(response, 'textarea[name="description"]') as (elem,):
            pass

        with self.assertHTML(response, '*[type="submit"]') as (elem,):
            pass

    def test_post(self):
        count = Jardin.objects.filter(proprietaire=self.adherant).count()

        jardin = self.adherant.jardin_set.first()
        params = {'pk': jardin.id}
        post_data = {
            'appelation': 'Nouveau jardin',
            'description': 'Bla bla bla',
            'exposition': '123',
            'type_sol': 'Sableux',
            'irrigation': 'Arrosoir',
            'mise_en_culture': '2014',
            'superficie': '150.0',
            'adresse': 'Au coin de la rue',
            'commune': 'Voiron',
            'latitude': '54.61353',
            'longitude': '45.38131',
            'altitude': '453'
        }
        url = reverse('s5appadherant:jardin_edit', kwargs=params)

        request = self.factory.post(url, data=post_data)
        request.user = self.adherant.user
        request.resolver_match = resolve(url)
        JardinEditView.as_view()(request, **params)

        post_edit_count = Jardin.objects.filter(proprietaire=self.adherant).count()

        self.assertEqual(count, post_edit_count)
        jardin_edited = self.adherant.jardin_set.first()
        self.assertEqual(jardin.id, jardin_edited.id)
        self.assertEqual('Nouveau jardin', jardin_edited.appelation)
        self.assertEqual('Bla bla bla', jardin_edited.description)
        self.assertEqual(123, jardin_edited.exposition)
        self.assertEqual('Sableux', jardin_edited.type_sol)
        self.assertEqual('Arrosoir', jardin_edited.irrigation)
        self.assertEqual(2014, jardin_edited.mise_en_culture)
        self.assertEqual(150.0, jardin_edited.superficie)
        self.assertEqual('Au coin de la rue', jardin_edited.adresse.adresse)
        self.assertEqual('Voiron', jardin_edited.adresse.commune)
        self.assertEqual(54.61353, jardin_edited.adresse.latitude)
        self.assertEqual(45.38131, jardin_edited.adresse.longitude)
        self.assertEqual(453, jardin_edited.adresse.altitude)



