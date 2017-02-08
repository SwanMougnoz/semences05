from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.test import RequestFactory
from django.test import TestCase
from django_dynamic_fixture import G

from s5appadherant.models import Cultivateur
from s5mailing.views.cultivateur import CultivateurMessageView, CultivateurRequestMessageView, \
    CultivateurAcceptMessageView, CultivateurDenyMessageView


class CultivateurMessageTestCase(TestCase):
    def setUp(self):
        self.cultivateur = G(Cultivateur)
        self.request = RequestFactory().get(reverse('s5appadherant:accueil'))
        self.request.user = G(User)


class CultivateurMessageViewTest(CultivateurMessageTestCase):

    def setUp(self):
        super(CultivateurMessageViewTest, self).setUp()
        self.message = CultivateurMessageView(self.cultivateur, self.request)

    def test_init(self):
        self.assertEqual(self.cultivateur, self.message.cultivateur)
        self.assertEqual(self.request, self.message.request)

    def test_get_context_data(self):
        context = self.message.get_context_data()
        self.assertDictContainsSubset({
            'cultivateur': self.cultivateur
        }, context)

    def test_get_recipient(self):
        with self.assertRaises(NotImplementedError):
            self.message.get_recipients()


class CultivateurRequestMessageViewTest(CultivateurMessageTestCase):

    def setUp(self):
        super(CultivateurRequestMessageViewTest, self).setUp()
        self.message = CultivateurRequestMessageView(self.cultivateur, self.request)

    def test_get_recipient(self):
        self.assertEqual((self.cultivateur.jardin.proprietaire.user.email,),
                         self.message.get_recipients())

    def test_render_to_message(self):
        rendered = self.message.render_to_message()
        self.assertIsInstance(rendered, EmailMultiAlternatives)
        self.assertEqual(self.message.get_recipients(), tuple(rendered.to))


class CultivateurAcceptMessageViewTest(CultivateurMessageTestCase):

    def setUp(self):
        super(CultivateurAcceptMessageViewTest, self).setUp()
        self.message = CultivateurAcceptMessageView(self.cultivateur, self.request)

    def test_get_recipient(self):
        self.assertEqual((self.cultivateur.adherant.user.email,),
                         self.message.get_recipients())

    def test_render_to_message(self):
        rendered = self.message.render_to_message()
        self.assertIsInstance(rendered, EmailMultiAlternatives)
        self.assertEqual(self.message.get_recipients(), tuple(rendered.to))


class CultivateurDenyMessageViewTest(CultivateurMessageTestCase):

    def setUp(self):
        super(CultivateurDenyMessageViewTest, self).setUp()
        self.message = CultivateurDenyMessageView(self.cultivateur, self.request)

    def test_get_recipient(self):
        self.assertEqual((self.cultivateur.adherant.user.email,),
                         self.message.get_recipients())

    def test_render_to_message(self):
        rendered = self.message.render_to_message()
        self.assertIsInstance(rendered, EmailMultiAlternatives)
        self.assertEqual(self.message.get_recipients(), tuple(rendered.to))
