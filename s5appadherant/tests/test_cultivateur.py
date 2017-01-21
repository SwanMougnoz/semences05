# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, resolve
from django.test import RequestFactory
from django.test import TestCase
from django_dynamic_fixture import G
from with_asserts.mixin import AssertHTMLMixin

from s5appadherant.models import Adherant, User, Jardin, Cultivateur
from views.cultivateur import CultivateurRequestView, CultivateurDecideView


# todo: mocker MailerService
class CultivateurRequestTest(TestCase, AssertHTMLMixin):

    def setUp(self):
        self.factory = RequestFactory()
        self.adherant = G(Adherant, user=G(User))
        self.proprietaire = G(Adherant, user=G(User))
        self.jardin = G(Jardin, proprietaire=self.proprietaire)

    def get(self, jardin):
        params = {'jardin_id': jardin.id}
        url = reverse('s5appadherant:cultivateur_request', kwargs=params)

        request = self.factory.get(url)
        request.user = self.adherant.user
        request.resolver_match = resolve(url)
        response = CultivateurRequestView.as_view()(request, **params)

        return response, url

    def test_get(self):
        response, url = self.get(self.jardin)

        self.assertEqual(200, response.status_code)
        response.render()

        with self.assertHTML(response, "form[action='%s'] button[type='submit']" % url):
            pass

    def test_get_pending(self):
        G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=False)

        response, url = self.get(self.jardin)
        self.assertEqual(302, response.status_code)

    def test_get_accepted(self):
        G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=True)

        response, url = self.get(self.jardin)
        self.assertEqual(302, response.status_code)

    def test_get_self_proprietaire(self):
        jardin = G(Jardin, proprietaire=self.adherant)

        response, url = self.get(jardin)
        self.assertEqual(302, response.status_code)

    def test_post(self):
        params = {'jardin_id': self.jardin.id}
        url = reverse('s5appadherant:cultivateur_request', kwargs=params)

        request = self.factory.post(url)
        request.user = self.adherant.user
        request.resolver_match = resolve(url)

        count = Cultivateur.objects.all().count()

        CultivateurRequestView.as_view()(request, **params)

        post_request_count = Cultivateur.objects.all().count()
        self.assertEqual(count + 1, post_request_count)

        cultivateur = Cultivateur.objects.all().order_by('-id').first()
        self.assertEqual(self.adherant, cultivateur.adherant)
        self.assertEqual(self.jardin, cultivateur.jardin)
        self.assertEqual(False, cultivateur.accepte)


class CultivateurDecideTest(TestCase, AssertHTMLMixin):

    def setUp(self):
        self.factory = RequestFactory()
        self.adherant = G(Adherant, user=G(User))
        self.proprietaire = G(Adherant, user=G(User))
        self.jardin = G(Jardin, proprietaire=self.proprietaire)

    def get(self, cultivateur):
        params = {'cultivateur_id': cultivateur.id}
        url = reverse('s5appadherant:cultivateur_decide', kwargs=params)

        request = self.factory.get(url)
        request.user = self.proprietaire.user
        request.resolver_match = resolve(url)
        response = CultivateurDecideView.as_view()(request, **params)

        return response, url

    def test_get(self):
        cultivateur = G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=False)

        response, url = self.get(cultivateur)

        self.assertEqual(200, response.status_code)
        response.render()

        with self.assertHTML(response, "form[action='%s'] button[name='cultivateur_accept']" % url):
            pass
        with self.assertHTML(response, "form[action='%s'] button[name='cultivateur_deny']" % url):
            pass

    def test_get_accepted(self):
        cultivateur = G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=True)

        response, url = self.get(cultivateur)
        self.assertEqual(302, response.status_code)

    def test_get_not_proprietaire(self):
        cultivateur = G(Cultivateur, jardin=G(Jardin), adherant=self.adherant, accepte=False)

        response, url = self.get(cultivateur)
        self.assertEqual(302, response.status_code)

    def test_get_self_adherant(self):
        cultivateur = G(Cultivateur, jardin=G(Jardin), adherant=self.proprietaire, accepte=False)

        response, url = self.get(cultivateur)
        self.assertEqual(302, response.status_code)

    def post_accept(self):
        cultivateur = G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=False)

        params = {'cultivateur_id': cultivateur.id}
        url = reverse('s5appadherant:cultivateur_decide', kwargs=params)

        request = self.factory.post(url)
        request.user = self.proprietaire.user
        request.resolver_match = resolve(url)
        request.POST.update({'cultivateur_accept': True})

        count = Cultivateur.objects.all().count()

        CultivateurDecideView.as_view()(request, **params)

        post_decide_count = Cultivateur.objects.all().count()

        cultivateur = Cultivateur.objects.get(pk=cultivateur.id)
        self.assertEqual(count, post_decide_count)
        self.assertTrue(cultivateur.accepte)

    def post_deny(self):
        cultivateur = G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=False)

        params = {'cultivateur_id': cultivateur.id}
        url = reverse('s5appadherant:cultivateur_decide', kwargs=params)

        request = self.factory.post(url)
        request.user = self.proprietaire.user
        request.resolver_match = resolve(url)
        request.POST.update({'cultivateur_deny': True})

        count = Cultivateur.objects.all().count()

        CultivateurDecideView.as_view()(request, **params)

        post_decide_count = Cultivateur.objects.all().count()

        self.assertEqual(count - 1, post_decide_count)
        with self.assertRaises(ObjectDoesNotExist):
            Cultivateur.objects.get(pk=cultivateur.id)


