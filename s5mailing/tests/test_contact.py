from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.test import TestCase

from s5mailing.views.contact import ContactMessageView, ContactCopyMessageView


class ContactMessageViewTest(TestCase):

    def setUp(self):
        self.message = ContactMessageView('Veillez, merci.', 'SVP.', 'jeanpierre@contact.com')

    def test_init(self):
        self.assertEqual('Veillez, merci.', self.message.subject)
        self.assertEqual('SVP.', self.message.message)
        self.assertEqual('jeanpierre@contact.com', self.message.sender)

    def test_get_context_data(self):
        context = self.message.get_context_data()
        self.assertDictContainsSubset({
            'subject': self.message.subject,
            'message': self.message.message,
            'sender': self.message.sender
        }, context)

    def test_render_to_message(self):
        rendered = self.message.render_to_message()
        self.assertIsInstance(rendered, EmailMultiAlternatives)
        self.assertEqual('%s' % self.message.subject, rendered.subject)
        self.assertEqual([settings.CONTACT_EMAIL], rendered.to)


class ContactCopyMessageViewTest(TestCase):

    def setUp(self):
        self.message = ContactCopyMessageView('Veillez, merci.', 'SVP.', 'jeanpierre@contact.com')

    def test_init(self):
        self.assertEqual('Veillez, merci.', self.message.subject)
        self.assertEqual('SVP.', self.message.message)
        self.assertEqual('jeanpierre@contact.com', self.message.sender)

    def test_get_context_data(self):
        context = self.message.get_context_data()
        self.assertDictContainsSubset({
            'subject': self.message.subject,
            'message': self.message.message
        }, context)

    def test_render_to_message(self):
        rendered = self.message.render_to_message()
        self.assertIsInstance(rendered, EmailMultiAlternatives)
        self.assertEqual('Re: %s (grainedesmontagnes.org)' % self.message.subject, rendered.subject)
        self.assertEqual([self.message.sender], rendered.to)
