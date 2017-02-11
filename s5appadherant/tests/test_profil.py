# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse, resolve
from django.test import RequestFactory
from django.test import TestCase
from django_dynamic_fixture import G
from with_asserts.mixin import AssertHTMLMixin

from s5appadherant.models import Adherant, User
from s5appadherant.views.profil import ProfilDetailView, ProfilEditView


class ProfilDetailTest(TestCase, AssertHTMLMixin):

    def setUp(self):
        self.factory = RequestFactory()
        self.adherant = G(Adherant, user=G(User))
        self.other_adherant = G(Adherant, user=G(User))

    def test_current(self):
        url = reverse('s5appadherant:profil_current')

        request = self.factory.get(url)
        request.user = self.adherant.user
        request.resolver_match = resolve(url)
        response = ProfilDetailView.as_view()(request)

        self.assertEqual(200, response.status_code)

        response.render()

        self.assertContains(response, self.adherant.user.first_name)
        self.assertContains(response, self.adherant.user.last_name)
        est_professionnel = 'Oui' if self.adherant.est_professionnel else 'Non'
        self.assertContains(response, est_professionnel)
        self.assertContains(response, self.adherant.telephone)
        self.assertContains(response, self.adherant.user.email)

        # Le document doit contenir un lien vers l'édition du profil
        edit_url = reverse('s5appadherant:profil_edit')
        with self.assertHTML(response, 'a[href="%s"]' % edit_url):
            pass

        with self.assertHTML(response, 'table#profiljardintable'):
            pass

    def test_get(self):
        params = {'adherant_id': self.other_adherant.id}
        url = reverse('s5appadherant:profil_detail', kwargs=params)

        request = self.factory.get(url)
        request.user = self.adherant.user
        request.resolver_match = resolve(url)
        response = ProfilDetailView.as_view()(request, **params)

        self.assertEqual(200, response.status_code)

        response.render()

        edit_url = reverse('s5appadherant:profil_edit')
        self.assertNotHTML(response, 'a[href="%s"]' % edit_url)


class ProfilEditTest(TestCase, AssertHTMLMixin):

    def setUp(self):
        self.factory = RequestFactory()
        self.adherant = G(Adherant, user=G(User))

    def test_get(self):
        url = reverse('s5appadherant:profil_edit')

        request = self.factory.get(url)
        request.user = self.adherant.user
        request.resolver_match = resolve(url)
        response = ProfilEditView.as_view()(request)

        self.assertEqual(200, response.status_code)

        response.render()

        expected_inputs = [
            'user-username',
            'user-email',
            'user-first_name',
            'user-last_name',
            'adherant-est_professionnel',
            'adherant-telephone',
            'adresse-adresse',
            'adresse-commune'
        ]

        for input_name in expected_inputs:
            with self.assertHTML(response, 'input[name="%s"]' % input_name):
                pass

        with self.assertHTML(response, 'select[name="adherant-experience"]'):
            pass

        # Le document doit contenir un lien vers le profil
        profil_url = reverse('s5appadherant:profil_current')
        with self.assertHTML(response, 'a[href="%s"]' % profil_url):
            pass

    def test_post(self):
        count = Adherant.objects.count()

        url = reverse('s5appadherant:profil_edit')
        post_data = {
            'user-username': 'newname',
            'user-email': 'new@email.com',
            'user-first_name': 'Toto',
            'user-last_name': 'Titi',
            'adherant-est_professionnel': True,
            'adherant-experience': 'confirme',
            'adherant-telephone': '0123456789',
            'adresse-adresse': '48 Rue de la soif',
            'adresse-commune': 'Rennes'
        }

        request = self.factory.post(url, data=post_data)
        request.user = self.adherant.user
        request.resolver_match = resolve(url)
        response = ProfilEditView.as_view()(request)

        post_add_count = Adherant.objects.count()
        adherant = Adherant.objects.get(pk=self.adherant.id)

        self.assertEqual(count, post_add_count)
        self.assertEqual('newname', adherant.user.username)
        self.assertEqual('new@email.com', adherant.user.email)
        self.assertEqual('Toto', adherant.user.first_name)
        self.assertEqual('Titi', adherant.user.last_name)
        self.assertEqual(True, adherant.est_professionnel)
        self.assertEqual('confirme', adherant.experience)
        self.assertEqual('0123456789', adherant.telephone)
        self.assertEqual('48 Rue de la soif', adherant.adresse.adresse)
        self.assertEqual('Rennes', adherant.adresse.commune)
