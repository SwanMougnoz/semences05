# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, AnonymousUser
from django.core.paginator import Page
from django.core.urlresolvers import reverse, resolve
from django.test import RequestFactory
from django.test import TestCase
from django_dynamic_fixture import G

from s5appadherant.forms.variete import VarieteForm
from s5appadherant.models import Variete, Adherant
from s5appadherant.views.variete import VarieteAddView, VarieteDetailView, VarieteEditView, VarieteListView


class VarieteListViewTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = G(User)

    def test_get(self):
        request = self.factory.get(reverse('s5appadherant:variete_list'))
        request.user = self.user
        response = VarieteListView.as_view()(request)

        # La page doit retourner la bonne template
        self.assertEqual(200, response.status_code)

        # Le context doit contenir un queryset paginé
        self.assertIsInstance(response.context_data['varietes'], Page)
        self.assertEqual(1, response.context_data['varietes'].number)

    def test_get_login_required(self):
        request = self.factory.get(reverse('s5appadherant:variete_list'))
        request.user = AnonymousUser()
        response = VarieteListView.as_view()(request)

        # La page ne doit pas être accessible
        self.assertEqual(302, response.status_code)


class VarieteDetailTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.adherant = G(Adherant, user=G(User))
        [G(Variete, id=i) for i in range(1, 5)]

    def get(self, user, params):
        url = reverse('s5appadherant:variete_detail', kwargs=params)
        request = self.factory.get(url)
        request.user = user
        request.resolver_match = resolve(reverse('s5appadherant:variete_detail', kwargs=params))
        return VarieteDetailView.as_view()(request, **params)

    def test_get(self):
        variete = Variete.objects.first()
        response = self.get(self.adherant.user, {
            'variete_id': variete.id
        })

        self.assertEqual(200, response.status_code)
        self.assertContains(response, variete.nom)
        self.assertContains(response, variete.description)
        self.assertContains(response, variete.photo.url)

    def test_get_not_found(self):
        response = self.get(self.adherant.user, {
            'variete_id': 666
        })
        self.assertEqual(404, response.status_code)

    def test_get_login_required(self):
        variete = Variete.objects.first()
        response = self.get(AnonymousUser(), {
            'variete_id': variete.id
        })
        self.assertEqual(302, response.status_code)


class VarieteAddTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.adherant = G(Adherant, user=G(User))

    def test_get(self):
        request = self.factory.get(reverse('s5appadherant:variete_new'))
        request.user = self.adherant.user
        response = VarieteAddView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context_data['form'], VarieteForm)

    def test_post(self):
        count = Variete.objects.count()

        request = self.factory.post(reverse('s5appadherant:variete_new'), data={
            'nom': 'Nouvelle variete',
            'description': 'Bla bla bla'
        })
        request.user = self.adherant.user
        VarieteAddView.as_view()(request)

        post_add_count = Variete.objects.count()
        variete = Variete.objects.all().order_by('-id')[0]

        self.assertEqual(count + 1, post_add_count)
        self.assertEqual('Nouvelle variete', variete.nom)
        self.assertEqual('Bla bla bla', variete.description)


class VarieteEditTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.adherant = G(Adherant, user=G(User))
        [G(Variete) for i in range(1, 5)]

    def test_get(self):
        params = {
            'pk': Variete.objects.first().id
        }
        request = self.factory.get(reverse('s5appadherant:variete_edit', kwargs=params))
        request.user = self.adherant.user
        response = VarieteEditView.as_view()(request, **params)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context_data['form'], VarieteForm)

    def test_post(self):
        variete = Variete.objects.first()
        params = {
            'pk': variete.id
        }
        url = reverse('s5appadherant:variete_edit', kwargs=params)

        request = self.factory.post(url, data={
            'nom': 'Nouveau nom',
            'description': 'Nouvelle description'
        })
        request.user = self.adherant.user

        count = Variete.objects.count()

        VarieteEditView.as_view()(request, **params)

        post_edit_count = Variete.objects.count()

        variete = Variete.objects.get(pk=variete.id)
        self.assertEqual(count, post_edit_count)
        self.assertEqual('Nouveau nom', variete.nom)
        self.assertEqual('Nouvelle description', variete.description)
