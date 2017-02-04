from mailviews.messages import TemplatedHTMLEmailMessageView


class CultivateurRequestMessageView(TemplatedHTMLEmailMessageView):
    subject_template_name = 's5mailing/subject/cultivateur_request.txt'
    body_template_name = 's5mailing/txt/cultivateur_request.txt'
    html_body_template_name = 's5mailing/html/cultivateur_request.html'

    def __init__(self, cultivateur):
        super(CultivateurRequestMessageView, self).__init__()
        self.cultivateur = cultivateur

    def get_context_data(self, **kwargs):
        context = super(CultivateurRequestMessageView, self).get_context_data(**kwargs)
        context['cultivateur'] = self.cultivateur
        return context

    def render_to_message(self, *args, **kwargs):
        assert 'to' not in kwargs
        kwargs['to'] = (self.cultivateur.jardin.proprietaire.user.email,)
        return super(CultivateurRequestMessageView, self).render_to_message(*args, **kwargs)
