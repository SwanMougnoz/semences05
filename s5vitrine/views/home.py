from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    Page d'accueil
    """

    template_name = 's5vitrine/home.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'menu_active': 'home'
        })
