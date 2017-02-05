from django.core.mail import EmailMultiAlternatives
from django.test import TestCase
from django_dynamic_fixture import G

from s5appadherant.models import Cultivateur
from s5mailing.views.cultivateur import CultivateurMessageView, CultivateurRequestMessageView, \
    CultivateurAcceptMessageView, CultivateurDenyMessageView


class CultivateurMessageViewTest(TestCase):

    def setUp(self):
        self.cultivateur = G(Cultivateur)
        self.message = CultivateurMessageView(self.cultivateur)

    def test_init(self):
        self.assertEqual(self.cultivateur, self.message.cultivateur)

    def test_get_context_data(self):
        context = self.message.get_context_data()
        self.assertDictContainsSubset({
            'cultivateur': self.cultivateur
        }, context)

    def test_get_recipient(self):
        with self.assertRaises(NotImplementedError):
            self.message.get_recipients()


class CultivateurRequestMessageViewTest(TestCase):

    def setUp(self):
        self.cultivateur = G(Cultivateur)
        self.message = CultivateurRequestMessageView(self.cultivateur)

    def test_get_recipient(self):
        self.assertEqual((self.cultivateur.jardin.proprietaire.user.email,),
                         self.message.get_recipients())

    def test_render_to_message(self):
        rendered = self.message.render_to_message()
        self.assertIsInstance(rendered, EmailMultiAlternatives)
        self.assertEqual(self.message.get_recipients(), tuple(rendered.to))


class CultivateurAcceptMessageViewTest(TestCase):

    def setUp(self):
        self.cultivateur = G(Cultivateur)
        self.message = CultivateurAcceptMessageView(self.cultivateur)

    def test_get_recipient(self):
        self.assertEqual((self.cultivateur.adherant.user.email,),
                         self.message.get_recipients())

    def test_render_to_message(self):
        rendered = self.message.render_to_message()
        self.assertIsInstance(rendered, EmailMultiAlternatives)
        self.assertEqual(self.message.get_recipients(), tuple(rendered.to))


class CultivateurDenyMessageViewTest(TestCase):

    def setUp(self):
        self.cultivateur = G(Cultivateur)
        self.message = CultivateurDenyMessageView(self.cultivateur)

    def test_get_recipient(self):
        self.assertEqual((self.cultivateur.adherant.user.email,),
                         self.message.get_recipients())

    def test_render_to_message(self):
        rendered = self.message.render_to_message()
        self.assertIsInstance(rendered, EmailMultiAlternatives)
        self.assertEqual(self.message.get_recipients(), tuple(rendered.to))
