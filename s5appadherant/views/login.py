from django.views.generic import TemplateView


class LoginView(TemplateView):

    template_name = "s5appadherant/login.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
