# -*- coding: utf-8 -*-
from actstream.models import Follow, Action
from django.core.urlresolvers import reverse, resolve
from django.test import RequestFactory
from django.test import TestCase
from django_dynamic_fixture import G, N
from with_asserts.mixin import AssertHTMLMixin

from s5appadherant.models import Adherant, User, Jardin, Cultivateur
from s5appadherant.views.cultivateur import CultivateurRequestView, CultivateurDecideView, CultivateurDeleteView
from s5appadherant import permissions


class CultivateurModelTest(TestCase):

    def setUp(self):
        self.proprietaire = G(Adherant)
        self.adherant = G(Adherant)
        self.jardin = G(Jardin, prorietaire=self.proprietaire)

        self.cultivateur = G(Cultivateur, jardin=self.jardin, adherant=self.adherant)

    def test_accept(self):
        self.cultivateur.accept()

        self.assertTrue(self.cultivateur.accepte)
        self.assertFalse(self.cultivateur.pending)

    def test_deny(self):
        self.cultivateur.deny()

        self.assertFalse(self.cultivateur.accepte)
        self.assertFalse(self.cultivateur.pending)


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
        G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=False, pending=True)

        response, url = self.get(self.jardin)
        self.assertEqual(302, response.status_code)

    def test_get_accepted(self):
        G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=True, pending=False)

        response, url = self.get(self.jardin)
        self.assertEqual(302, response.status_code)

    def test_get_refused(self):
        G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=False, pending=False)

        response, url = self.get(self.jardin)
        self.assertEqual(200, response.status_code)

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
        self.assertFalse(cultivateur.accepte)
        self.assertTrue(cultivateur.pending)

        self.assertFalse(self.adherant.user.has_perm('s5appadherant.change_jardin', self.jardin))
        self.assertFalse(self.adherant.user.has_perm('s5appadherant.request_cultivateur', self.jardin))
        self.assertTrue(Follow.objects.is_following(self.adherant.user, cultivateur))


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

    def post(self, cultivateur, choice):
        params = {'cultivateur_id': cultivateur.id}
        url = reverse('s5appadherant:cultivateur_decide', kwargs=params)

        request = self.factory.post(url)
        request.user = self.proprietaire.user
        request.resolver_match = resolve(url)
        request.POST.update({choice: True})

        CultivateurDecideView.as_view()(request, **params)

    def test_get(self):
        cultivateur = G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=False, pending=True)

        response, url = self.get(cultivateur)

        self.assertEqual(200, response.status_code)
        response.render()

        with self.assertHTML(response, "form[action='%s'] button[name='cultivateur_accept']" % url):
            pass
        with self.assertHTML(response, "form[action='%s'] button[name='cultivateur_deny']" % url):
            pass

    def test_get_accepted(self):
        cultivateur = G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=True, pending=False)

        response, url = self.get(cultivateur)
        self.assertEqual(302, response.status_code)

    def test_get_refused(self):
        cultivateur = G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=False, pending=False)

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

    def test_post_accept(self):
        cultivateur = G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=False)
        self.post(cultivateur, 'cultivateur_accept')

        cultivateur = Cultivateur.objects.get(pk=cultivateur.id)
        self.assertTrue(cultivateur.accepte)
        self.assertFalse(cultivateur.pending)

        self.assertTrue(self.adherant.user.has_perm('s5appadherant.change_jardin', self.jardin))
        self.assertFalse(self.adherant.user.has_perm('s5appadherant.request_cultivateur', self.jardin))

        self.assertTrue(Follow.objects.is_following(self.adherant.user, self.jardin))

    def test_post_deny(self):
        cultivateur = G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=False)
        self.post(cultivateur, 'cultivateur_deny')

        cultivateur = Cultivateur.objects.get(pk=cultivateur.id)
        self.assertFalse(cultivateur.accepte)
        self.assertFalse(cultivateur.pending)

        self.assertFalse(self.adherant.user.has_perm('s5appadherant.change_jardin', self.jardin))
        self.assertTrue(self.adherant.user.has_perm('s5appadherant.request_cultivateur', self.jardin))

        self.assertFalse(Follow.objects.is_following(self.adherant.user, self.jardin))


class CultivateurDeleteTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.proprietaire = G(Adherant)
        self.adherant = G(Adherant)
        self.jardin = G(Jardin, proprietaire=self.proprietaire)

    def get(self, cultivateur, user):
        params = {'jardin_id': self.jardin.id, 'cultivateur_id': cultivateur.id}
        request = self.factory.get(reverse('s5appadherant:cultivateur_delete', kwargs=params))
        request.user = user

        return CultivateurDeleteView.as_view()(request, **params)

    def test_get(self):
        cultivateur = G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=True)
        response = self.get(cultivateur, self.proprietaire.user)

        cultivateur_loaded = Cultivateur.objects.get(pk=cultivateur.id)

        self.assertEqual(302, response.status_code)
        self.assertFalse(cultivateur_loaded.accepte)
        self.assertFalse(Follow.objects.is_following(cultivateur.adherant.user, self.jardin))
        self.assertFalse(cultivateur.adherant.user.has_perm('s5appadherant:change_jardin', self.jardin))

    def test_get_cultivateur(self):
        cultivateur = G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=True)
        response = self.get(cultivateur, self.adherant.user)

        self.assertEqual(302, response.status_code)

        cultivateur_loaded = Cultivateur.objects.get(pk=cultivateur.id)

    def test_get_guest(self):
        pass

    def test_get_inexistant(self):
        pass

    def test_get_jardin_cultivateur_doesnt_match(self):
        pass

    def test_get_refused(self):
        pass

    def test_get_pending(self):
        pass


class CultivateurManagerTest(TestCase):
    def setUp(self):
        self.jardin = G(Jardin)
        self.accepte = G(Cultivateur, adherant=G(Adherant), jardin=self.jardin, accepte=True, pending=False)
        self.pending = G(Cultivateur, adherant=G(Adherant), jardin=self.jardin, accepte=False, pending=True)
        self.refused = G(Cultivateur, adherant=G(Adherant), jardin=self.jardin, accepte=False, pending=False)

    def test_accepte(self):
        cultivateurs = Cultivateur.objects.accepte()
        self.assertEqual(1, len(cultivateurs))
        self.assertEqual(self.accepte, cultivateurs.first())