# -*- coding: utf-8 -*-

from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Page
from django.core.urlresolvers import reverse, resolve
from django.test import RequestFactory
from django.test import TestCase
from with_asserts.mixin import AssertHTMLMixin
from django_dynamic_fixture import G

from s5appadherant.forms.adresse import AdresseFullForm
from s5appadherant.forms.jardin import JardinForm
from s5appadherant.models import Adherant, Jardin, User, Cultivateur
from s5appadherant.views.jardin import JardinListView, JardinDetailView, JardinAddView, JardinEditView, \
    JardinAdherantListView, JardinCultivateurListView


class JardinListTest(TestCase, AssertHTMLMixin):

    def setUp(self):
        self.factory = RequestFactory()
        self.adherant = G(Adherant, user=G(User))
        self.cultivateur = G(Adherant, user=G(User))

        jardin = G(Jardin, proprietaire=self.adherant)
        [G(Jardin) for i in range(1, 5)]
        G(Cultivateur, jardin=jardin, adherant=self.cultivateur, accepte=True, pending=False)

    def _do_test_jardin_list(self, response, jardins):
        self.assertEqual(200, response.status_code)

        # Le context doit contenir un queryset paginé
        self.assertIsInstance(response.context_data['jardins'], Page)
        self.assertEqual(1, response.context_data['jardins'].number)

        response.render()
        jardin_count = len(jardins)

        # Tous les jardins et uniquement les jardins de l'adherant doivent être sur la page
        # et contenir un lien vers leur détail
        with self.assertHTML(response, '.jardin-list .list-group-item') as (elems):
            self.assertEqual(jardin_count, len(elems))

        for jardin in jardins:
            detail_url = reverse('s5appadherant:jardin_detail', kwargs={
                'jardin_id': jardin.id
            })
            with self.assertHTML(response, 'a[href="%s"]' % detail_url):
                pass

        # Un lien vers la page d'ajout d'un jardin doit être présent
        add_url = reverse('s5appadherant:jardin_new')
        with self.assertHTML(response, 'a[href="%s"]' % add_url):
            pass

    def test_get_all(self):
        url = reverse('s5appadherant:jardin_all')

        request = self.factory.get(url)
        request.user = self.adherant.user
        request.resolver_match = resolve(url)
        response = JardinListView.as_view()(request)

        self._do_test_jardin_list(response, Jardin.objects.all())

    def test_get_adherant(self):
        params = {'adherant_id': self.adherant.id}
        url = reverse('s5appadherant:jardin_adherant', kwargs=params)

        request = self.factory.get(url)
        request.user = self.adherant.user
        request.resolver_match = resolve(url)
        response = JardinAdherantListView.as_view()(request, **params)

        self._do_test_jardin_list(response, Jardin.objects.filter(proprietaire=self.adherant))

    def test_get_cultivateur(self):
        params = {'adherant_id': self.cultivateur.id}
        url = reverse('s5appadherant:jardin_adherant', kwargs=params)

        request = self.factory.get(url)
        request.user = self.cultivateur.user
        request.resolver_match = resolve(url)
        response = JardinCultivateurListView.as_view()(request, **params)

        self._do_test_jardin_list(response, Jardin.objects.filter(cultivateur__adherant=self.cultivateur,
                                                                  cultivateur__accepte=True))

    def test_get_login_required(self):
        request = self.factory.get(reverse('s5appadherant:jardin_all'))
        request.user = AnonymousUser()
        response = JardinListView.as_view()(request)

        # La page ne doit pas être accessible
        self.assertEqual(302, response.status_code)


class JardinDetailTest(TestCase, AssertHTMLMixin):

    def setUp(self):
        self.factory = RequestFactory()
        self.proprietaire = G(Adherant)
        self.jardin = G(Jardin, proprietaire=self.proprietaire)

    def get(self, user):
        params = {'jardin_id': self.jardin.id}
        url = reverse('s5appadherant:jardin_detail', kwargs=params)

        request = self.factory.get(url)
        request.user = user
        request.resolver_match = resolve(url)
        return JardinDetailView.as_view()(request, **params)

    def _assert_jardin_detail(self, response):
        self.assertEqual(200, response.status_code)
        response.render()

        # Le document doit contenir toutes les informations relative au jardin
        self.assertContains(response, self.jardin.adresse.commune)
        self.assertContains(response, "%s m" % self.jardin.adresse.altitude)
        self.assertContains(response, self.jardin.appelation)
        self.assertContains(response, self.jardin.exposition)
        self.assertContains(response, self.jardin.type_sol)
        self.assertContains(response, '%s m²' % str(self.jardin.superficie).replace('.', ','))
        self.assertContains(response, self.jardin.irrigation)
        self.assertContains(response, self.jardin.mise_en_culture)
        self.assertContains(response, self.jardin.description)

    def _do_test_jardin_with_edit_permission(self, response):
        self._assert_jardin_detail(response)

        # Le document doit contenir une table des variétés cultivé
        with self.assertHTML(response, 'table#culturetablecultivateur'):
            pass

        # Le document doit contenir un lien vers la page d'édition de ce jardin
        edit_url = reverse('s5appadherant:jardin_edit', kwargs={
            'jardin_id': self.jardin.id
        })
        with self.assertHTML(response, 'a[href="%s"]' % edit_url):
            pass

        # Lien pour ajouter une culture
        culture_add_url = reverse('s5appadherant:culture_new', kwargs={
            'jardin_id': self.jardin.id
        })
        with self.assertHTML(response, 'a[href="%s"]' % culture_add_url):
            pass

        # Lien pour faire une demande d'ajout
        cultivateur_request_url = reverse('s5appadherant:cultivateur_request', kwargs={
            'jardin_id': self.jardin.id
        })
        self.assertNotHTML(response, 'a[href="%s"]' % cultivateur_request_url)

    def test_get_proprietaire(self):
        response = self.get(self.proprietaire.user)
        self._do_test_jardin_with_edit_permission(response)

    def test_get_proprietaire_with_cultivateurs(self):
        cultivateur_accepte = G(Cultivateur, jardin=self.jardin, adherant=G(Adherant), accepte=True, pending=False)
        cultivateur_pending = G(Cultivateur, jardin=self.jardin, adherant=G(Adherant), accepte=False, pending=True)
        cultivateur_refused = G(Cultivateur, jardin=self.jardin, adherant=G(Adherant), accepte=False, pending=False)

        response = self.get(self.proprietaire.user)
        response.render()

        with self.assertHTML(response, "#cultivateurs-list ul li") as elems:
            self.assertEqual(2, len(elems))

        delete_accepte_url = reverse('s5appadherant:cultivateur_delete', kwargs={
            'jardin_id': self.jardin.id,
            'cultivateur_id': cultivateur_accepte.id
        })
        with self.assertHTML(response, 'a[href="%s"]' % delete_accepte_url) as elems:
            self.assertEqual(1, len(elems))

    def test_get_cultivateur(self):
        adherant = G(Adherant)
        cultivateur = G(Cultivateur, jardin=self.jardin, adherant=adherant, accepte=True, pending=False)

        response = self.get(adherant.user)

        self._do_test_jardin_with_edit_permission(response)

        cultivateur_quit_url = reverse('s5appadherant:cultivateur_quit', kwargs={
            'jardin_id': self.jardin.id,
            'cultivateur_id': cultivateur.id
        })
        with self.assertHTML(response, 'a[href="%s"]' % cultivateur_quit_url):
            pass

    def test_get_adherant(self):
        response = self.get(G(Adherant).user)
        self._assert_jardin_detail(response)

        # Le document doit contenir une table des variétés cultivé sans les actions cultivateur
        with self.assertHTML(response, 'table#culturetable'):
            pass

        # Le document ne doit pas contenir un lien vers la page d'édition de ce jardin
        edit_url = reverse('s5appadherant:jardin_edit', kwargs={
            'jardin_id': self.jardin.id
        })
        self.assertNotHTML(response, 'a[href="%s"]' % edit_url)

        # Lien pour ajouter une culture
        culture_add_url = reverse('s5appadherant:culture_new', kwargs={
            'jardin_id': self.jardin.id
        })
        self.assertNotHTML(response, 'a[href="%s"]' % culture_add_url)

        # Lien pour faire une demande d'ajout
        cultivateur_request_url = reverse('s5appadherant:cultivateur_request', kwargs={
            'jardin_id': self.jardin.id
        })
        with self.assertHTML(response, 'a[href="%s"]' % cultivateur_request_url):
            pass

    def test_get_cultivateur_pending(self):
        adherant = G(Adherant)
        G(Cultivateur, jardin=self.jardin, adherant=adherant, accepte=False, pending=True)

        response = self.get(adherant.user)
        response.render()

        # Il ne doit y avoir de lien pour faire une nouvelle demande
        cultivateur_request_url = reverse('s5appadherant:cultivateur_request', kwargs={
            'jardin_id': self.jardin.id
        })
        self.assertNotHTML(response, 'a[href="%s"]' % cultivateur_request_url)

    def test_get_cultivateur_refused(self):
        adherant = G(Adherant)
        G(Cultivateur, jardin=self.jardin, adherant=adherant, accepte=False, pending=False)

        response = self.get(adherant.user)
        response.render()

        # Il doit y avoir un lien pour faire une nouvelle demande
        cultivateur_request_url = reverse('s5appadherant:cultivateur_request', kwargs={
            'jardin_id': self.jardin.id
        })
        with self.assertHTML(response, 'a[href="%s"]' % cultivateur_request_url):
            pass


class JardinAddTest(TestCase, AssertHTMLMixin):

    def setUp(self):
        self.factory = RequestFactory()
        self.adherant = G(Adherant, user=G(User))
        [G(Jardin) for i in range(1, 5)]

    def test_get(self):
        url = reverse('s5appadherant:jardin_new')

        request = self.factory.get(url)
        request.user = self.adherant.user
        request.resolver_match = resolve(url)
        response = JardinAddView.as_view()(request)

        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.context_data['jardin_form'], JardinForm)
        self.assertIsInstance(response.context_data['adresse_form'], AdresseFullForm)

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
            with self.assertHTML(response, 'input[name="%s"]' % input_elem):
                pass
        with self.assertHTML(response, 'textarea[name="description"]'):
            pass

        with self.assertHTML(response, '*[type="submit"]'):
            pass

    def test_post(self):
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

        count = Jardin.objects.all().count()
        count_adherant = Jardin.objects.filter(proprietaire=self.adherant).count()

        JardinAddView.as_view()(request)

        post_add_count = Jardin.objects.all().count()
        post_add_count_adherant = Jardin.objects.filter(proprietaire=self.adherant).count()

        jardin = Jardin.objects.all().order_by('-id')[0]

        self.assertEqual(count + 1, post_add_count)
        self.assertEqual(count_adherant + 1, post_add_count_adherant)

        self.assertEqual('Nouveau jardin', jardin.appelation)
        self.assertEqual('Bla bla bla', jardin.description)
        self.assertEqual('123', jardin.exposition)
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

    def setUp(self):
        self.factory = RequestFactory()
        self.adherant = G(Adherant, user=G(User))
        self.jardin = G(Jardin, proprietaire=self.adherant)

    def test_get(self):
        params = {'jardin_id': self.jardin.id}
        url = reverse('s5appadherant:jardin_edit', kwargs=params)

        request = self.factory.get(url)
        request.user = self.adherant.user
        request.resolver_match = resolve(url)
        response = JardinEditView.as_view()(request, **params)

        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.context_data['jardin_form'], JardinForm)
        self.assertIsInstance(response.context_data['adresse_form'], AdresseFullForm)

        response.render()

        # Le document doit contenir tous les champs de JardinForm
        expected_inputs = {
            'appelation': self.jardin.appelation,
            'exposition': self.jardin.exposition,
            'type_sol': self.jardin.type_sol,
            'irrigation': self.jardin.irrigation,
            'mise_en_culture': self.jardin.mise_en_culture,
            'superficie': self.jardin.superficie,
            'adresse': self.jardin.adresse.adresse,
            'commune': self.jardin.adresse.commune,
            'latitude': self.jardin.adresse.latitude,
            'longitude': self.jardin.adresse.longitude,
            'altitude': self.jardin.adresse.altitude
        }

        for input_elem, expected_value in expected_inputs.items():
            with self.assertHTML(response, 'input[name="%s"]' % input_elem) as (elem,):
                if expected_value is not None:
                    expected_value = str(expected_value)
                self.assertEqual(expected_value, elem.value)

        with self.assertHTML(response, 'textarea[name="description"]'):
            pass

        with self.assertHTML(response, '*[type="submit"]'):
            pass

    def test_post(self):

        params = {'jardin_id': self.jardin.id}
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

        count = Jardin.objects.all().count()
        count_adherant = Jardin.objects.filter(proprietaire=self.adherant).count()

        JardinEditView.as_view()(request, **params)

        post_edit_count = Jardin.objects.all().count()
        post_edit_count_adherant = Jardin.objects.filter(proprietaire=self.adherant).count()

        self.assertEqual(count, post_edit_count)
        self.assertEqual(count_adherant, post_edit_count_adherant)

        jardin_edited = Jardin.objects.get(pk=self.jardin.id)
        self.assertEqual('Nouveau jardin', jardin_edited.appelation)
        self.assertEqual('Bla bla bla', jardin_edited.description)
        self.assertEqual('123', jardin_edited.exposition)
        self.assertEqual('Sableux', jardin_edited.type_sol)
        self.assertEqual('Arrosoir', jardin_edited.irrigation)
        self.assertEqual(2014, jardin_edited.mise_en_culture)
        self.assertEqual(150.0, jardin_edited.superficie)
        self.assertEqual('Au coin de la rue', jardin_edited.adresse.adresse)
        self.assertEqual('Voiron', jardin_edited.adresse.commune)
        self.assertEqual(54.61353, jardin_edited.adresse.latitude)
        self.assertEqual(45.38131, jardin_edited.adresse.longitude)
        self.assertEqual(453, jardin_edited.adresse.altitude)



