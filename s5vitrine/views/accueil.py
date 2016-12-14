from django.views.generic import TemplateView
from s5vitrine.models.menuitem import Menuitem


class AccueilView(TemplateView):
    """
    Page d'accueil
    """

    template_name = 's5vitrine/accueil.html'

    def get(self, request, *args, **kwargs):

        menuitem = Menuitem.objects.get(pk='accueil')

        return self.render_to_response({
            'menu_actif': menuitem,
            'titre_page': 'Accueil - Reseau semences Hautes-Alpes'
        })
