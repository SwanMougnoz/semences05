from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.views.generic import TemplateView
from s5vitrine.models import PageContenu


class ContenuView(TemplateView):

    template_name = "s5vitrine/contenu.html"

    def get(self, request, *args, **kwargs):
        contenu_id = kwargs.get('contenu_id', None)
        try:
            contenu = PageContenu.objects.get(pk=contenu_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("<h1>La page demandee n'existe pas</h1>")

        return self.render_to_response({
            'contenu': contenu,
            'titre_page': contenu.titre,
            'menu_actif': contenu.menuitem
        })
