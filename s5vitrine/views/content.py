from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.views.generic import TemplateView
from s5vitrine.models import PageContenu


class ContentView(TemplateView):

    template_name = "s5vitrine/content.html"

    def get(self, request, *args, **kwargs):
        content_id = kwargs.get('content_id', None)
        try:
            contenu = PageContenu.objects.get(pk=content_id)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("<h1>La page demandee n'existe pas</h1>")

        return self.render_to_response({
            'contenu': contenu,
            'titre_page': contenu.titre_page
        })
