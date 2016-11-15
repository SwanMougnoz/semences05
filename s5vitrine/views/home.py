from django.views.generic import TemplateView
from s5vitrine.models import Menuitem


class HomeView(TemplateView):
    """
    Page d'accueil
    """

    template_name = 's5vitrine/home.html'

    def get(self, request, *args, **kwargs):

        menuitem = Menuitem.objects.get(pk='home')

        return self.render_to_response({
            'menu_active': menuitem,
            'titre_page': 'Accueil - Reseau semences Hautes-Alpes'
        })
