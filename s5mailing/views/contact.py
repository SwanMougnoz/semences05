from mailviews.messages import TemplatedHTMLEmailMessageView

from django.conf import settings


class ContactMessageView(TemplatedHTMLEmailMessageView):
    subject_template_name = 's5mailing/subject/contact.txt'
    body_template_name = 's5mailing/txt/contact.txt'
    html_body_template_name = 's5mailing/html/contact.html'

    def __init__(self, subject, message, sender):
        super(ContactMessageView, self).__init__()
        self.subject = subject
        self.message = message
        self.sender = sender

    def get_context_data(self, **kwargs):
        context = super(ContactMessageView, self).get_context_data(**kwargs)
        context.update({
            'subject': self.subject,
            'message': self.message,
            'sender': self.sender
        })
        return context

    def render_to_message(self, *args, **kwargs):
        assert 'to' not in kwargs
        kwargs['to'] = (settings.CONTACT_EMAIL,)
        return super(ContactMessageView, self).render_to_message(*args, **kwargs)


class ContactCopyMessageView(TemplatedHTMLEmailMessageView):
    subject_template_name = 's5mailing/subject/contact_copy.txt'
    body_template_name = 's5mailing/txt/contact_copy.txt'
    html_body_template_name = 's5mailing/html/contact_copy.html'

    def __init__(self, subject, message, sender):
        super(ContactCopyMessageView, self).__init__()
        self.sender = sender
        self.message = message
        self.subject = subject

    def get_context_data(self, **kwargs):
        context = super(ContactCopyMessageView, self).get_context_data(**kwargs)
        context['subject'] = self.subject
        context['message'] = self.message
        return context

    def render_to_message(self, *args, **kwargs):
        assert 'to' not in kwargs
        kwargs['to'] = (self.sender,)
        return super(ContactCopyMessageView, self).render_to_message(*args, **kwargs)
