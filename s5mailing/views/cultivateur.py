from mailviews.messages import TemplatedHTMLEmailMessageView


class CultivateurMessageView(TemplatedHTMLEmailMessageView):

    def __init__(self, cultivateur):
        super(CultivateurMessageView, self).__init__()
        self.cultivateur = cultivateur

    def get_context_data(self, **kwargs):
        context = super(CultivateurMessageView, self).get_context_data(**kwargs)
        context['cultivateur'] = self.cultivateur
        return context

    def get_recipients(self):
        raise NotImplemented

    def render_to_message(self, *args, **kwargs):
        assert 'to' not in kwargs
        kwargs['to'] = self.get_recipients()
        return super(CultivateurMessageView, self).render_to_message(*args, **kwargs)


class CultivateurRequestMessageView(CultivateurMessageView):
    subject_template_name = 's5mailing/subject/cultivateur_request.txt'
    body_template_name = 's5mailing/txt/cultivateur_request.txt'
    html_body_template_name = 's5mailing/html/cultivateur_request.html'

    def get_recipients(self):
        return self.cultivateur.jardin.proprietaire.user.email,


class CultivateurAcceptMessageView(CultivateurMessageView):
    subject_template_name = 's5mailing/subject/cultivateur_accept.txt'
    body_template_name = 's5mailing/txt/cultivateur_accept.txt'
    html_body_template_name = 's5mailing/html/cultivateur_accept.html'

    def get_recipients(self):
        return self.cultivateur.adherant.user.email,


class CultivateurDenyMessageView(CultivateurMessageView):
    subject_template_name = 's5mailing/subject/cultivateur_deny.txt'
    body_template_name = 's5mailing/txt/cultivateur_deny.txt'
    html_body_template_name = 's5mailing/html/cultivateur_deny.html'

    def get_recipients(self):
        return self.cultivateur.adherant.user.email,
