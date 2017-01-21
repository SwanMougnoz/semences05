# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template


class Mail(object):

    def __init__(self, **kwargs):
        self.subject = kwargs.get('subject', None)
        self.text_content = kwargs.get('text_content', None)
        self.html_content = kwargs.get('html_content', None)
        self.sender = kwargs.get('sender', None)
        self.recipients = kwargs.get('recipients', [])

    def _send(self):
        msg = EmailMultiAlternatives(self.subject, self.text_content, self.sender, self.recipients)
        if self.html_content is not None:
            msg.attach_alternative(self.html_content, "text/html")

        return msg.send()

    @staticmethod
    def render(template, context):
        content = get_template(template)
        return content.render(Context(context))


class CultivateurRequest(Mail):
    html_template = 's5appadherant/cultivateur/mails/html/request.html'
    text_template = 's5appadherant/cultivateur/mails/txt/request.txt'

    def send(self, cultivateur):
        adherant = cultivateur.adherant
        proprietaire = cultivateur.jardin.proprietaire

        subject_str = u"%s %s vous à adressé une demande pour cultiver votre jardin"
        text_content = self.render(self.text_template, {})
        html_content = self.render(self.html_template, {})

        self.subject = subject_str % (adherant.user.first_name, adherant.user.last_name)
        self.text_content = text_content
        self.html_content = html_content
        self.sender = "some email"
        self.recipients = [proprietaire.user.email]

        return self._send()


class CultivateurAccept(Mail):
    html_template = 's5appadherant/cultivateur/mails/html/accept.html'
    text_template = 's5appadherant/cultivateur/mails/txt/accept.txt'

    def send(self, cultivateur):
        adherant = cultivateur.adherant
        proprietaire = cultivateur.jardin.proprietaire

        subject_str = u"%s %s a accepté votre demande pour cultiver son jardin"
        text_content = self.render(self.text_template, {})
        html_content = self.render(self.html_template, {})

        self.subject = subject_str % (proprietaire.user.first_name, proprietaire.user.last_name)
        self.text_content = text_content
        self.html_content = html_content
        self.sender = "some email"
        self.recipients = [adherant.user.email]

        return self._send()


class CultivateurDeny(Mail):
    html_template = 's5appadherant/cultivateur/mails/html/deny.html'
    text_template = 's5appadherant/cultivateur/mails/txt/deny.txt'

    def send(self, cultivateur):
        adherant = cultivateur.adherant
        proprietaire = cultivateur.jardin.proprietaire

        subject_str = u"%s %s a accepté votre demande pour cultiver son jardin"
        text_content = self.render(self.text_template, {})
        html_content = self.render(self.html_template, {})

        self.subject = subject_str % (proprietaire.user.first_name, proprietaire.user.last_name)
        self.text_content = text_content
        self.html_content = html_content
        self.sender = "some email"
        self.recipients = [adherant.user.email]

        return self._send()


class MailDoesntExist(Exception):
    pass


class MailFactory(object):

    mails = {
        'cultivateur_request': CultivateurRequest,
        'cultivateur_accept': CultivateurAccept,
        'cultivateur_deny': CultivateurDeny
    }

    @staticmethod
    def send(identifier, *args, **kwargs):
        if identifier in MailFactory.mails.keys():
            mail = MailFactory.mails.get(identifier)()
            return mail.send(*args, **kwargs)
        else:
            raise MailDoesntExist("Aucun mail nommé '%s'" % identifier)
