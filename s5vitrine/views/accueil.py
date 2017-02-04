from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView

from s5vitrine.models import Menuitem


class AccueilView(TemplateView):
    """
    Page d'accueil
    """

    template_name = 's5vitrine/accueil.html'

    def get(self, request, *args, **kwargs):
        menuitem = Menuitem.objects.get(pk='accueil')

        try:
            qui_sommes_nous = Menuitem.objects.get(identifiant='qui-sommes-nous')
            qsm_url = qui_sommes_nous.page.url
        except ObjectDoesNotExist:
            qsm_url = '#'

        return self.render_to_response({
            'menu_actif': menuitem,
            'qui_sommes_nous_url': qsm_url,
            'titre_page': 'Accueil - Reseau semences Hautes-Alpes'
        })
