# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template


class Mail(object):

    @staticmethod
    def _send(subject, text_content, html_content, sender, recipient):
        msg = EmailMultiAlternatives(subject, text_content, sender, recipient)
        if html_content is not None:
            msg.attach_alternative(html_content, "text/html")

        return msg.send()

    @staticmethod
    def render(template, context):
        content = get_template(template)
        return content.render(Context(context))


class CultivateurRequest(Mail):
    html_template = 's5appadherant/cultivateur/mails/request.html'
    text_template = 's5appadherant/cultivateur/mails/request.txt'

    def send(self, cultivateur):
        adherant = cultivateur.adherant
        proprietaire = cultivateur.jardin.proprietaire

        subject_str = u"%s %s vous à adressé une demande pour cultiver votre jardin"
        subject = subject_str % (adherant.user.first_name, adherant.user.last_name)

        text_content = self.render(self.text_template, {})
        html_content = self.render(self.html_template, {})

        return self._send(subject, text_content, html_content, settings.MAILS.get('NOREPLY'), [proprietaire.user.email])


class MailDoesntExist(Exception):
    pass


class MailFactory(object):

    mails = {
        'cultivateur_request': CultivateurRequest
    }

    @staticmethod
    def send(identifier, *args, **kwargs):
        if identifier in MailFactory.mails.keys():
            mail = MailFactory.mails.get(identifier)()
            return mail.send(*args, **kwargs)
        else:
            raise MailDoesntExist("Aucun mail nommé '%s'" % identifier)
