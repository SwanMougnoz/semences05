# -*- coding: utf-8 -*-
from actstream.models import Follow, Action
from django.core.urlresolvers import reverse, resolve
from django.test import RequestFactory
from django.test import TestCase
from django_dynamic_fixture import G, N
from with_asserts.mixin import AssertHTMLMixin

from s5appadherant.models import Adherant, User, Jardin, Cultivateur
from s5appadherant.views.cultivateur import CultivateurRequestView, CultivateurDecideView
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


class CultivateurSignalsTest(TestCase):

    def setUp(self):
        self.proprietaire = G(Adherant)
        self.adherant = G(Adherant)
        self.jardin = G(Jardin, proprietaire=self.proprietaire)

        self.cultivateur = N(Cultivateur, jardin=self.jardin, adherant=self.adherant)

    def test_save_action_created(self):
        self.cultivateur.save()

        Action.objects.get_by_terms(verb='request', action_object=self.cultivateur)
        self.assertTrue(Follow.objects.is_following(self.proprietaire.user, self.cultivateur))
        self.assertTrue(Follow.objects.is_following(self.adherant.user, self.cultivateur))

    def test_save_action_updated_accept(self):
        self.cultivateur.save()
        self.cultivateur.accept()

        Action.objects.get_by_terms(verb="accept", action_object=self.cultivateur)
        request = Action.objects.get_by_terms(verb='request', action_object=self.cultivateur)
        self.assertIn(request, self.proprietaire.processed_actions.all())
        self.assertTrue(Follow.objects.is_following(self.adherant.user, self.jardin))

    def test_save_action_updated_deny(self):
        self.cultivateur.save()
        self.cultivateur.deny()

        Action.objects.get_by_terms(verb="deny", action_object=self.cultivateur)
        request = Action.objects.get_by_terms(verb='request', action_object=self.cultivateur)
        self.assertIn(request, self.proprietaire.processed_actions.all())
        self.assertFalse(Follow.objects.is_following(self.adherant.user, self.jardin))

    def test_save_action_updated_missing_request(self):
        self.cultivateur.save()
        request = Action.objects.get_by_terms(verb='request', action_object=self.cultivateur)
        request.delete()

        self.cultivateur.accept()
        self.assertTrue(Follow.objects.is_following(self.adherant.user, self.jardin))


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

    def post_accept(self):
        cultivateur = G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=False)
        self.post(cultivateur, 'cultivateur_accept')

        cultivateur = Cultivateur.objects.get(pk=cultivateur.id)
        self.assertTrue(cultivateur.accepte)
        self.assertFalse(cultivateur.pending)

        self.assertTrue(self.adherant.user.has_perm('s5appadherant.change_jardin', self.jardin))
        self.assertFalse(self.adherant.user.has_perm('s5appadherant.request_cultivateur', self.jardin))

        self.assertTrue(Follow.objects.is_following(self.adherant.user, self.jardin))

    def post_deny(self):
        cultivateur = G(Cultivateur, jardin=self.jardin, adherant=self.adherant, accepte=False)
        self.post(cultivateur, 'cultivateur_deny')

        cultivateur = Cultivateur.objects.get(pk=cultivateur.id)
        self.assertFalse(cultivateur.accepte)
        self.assertFalse(cultivateur.pending)

        self.assertFalse(self.adherant.user.has_perm('s5appadherant.change_jardin', self.jardin))
        self.assertTrue(self.adherant.user.has_perm('s5appadherant.request_cultivateur', self.jardin))

        self.assertFalse(Follow.objects.is_following(self.adherant.user, self.jardin))


