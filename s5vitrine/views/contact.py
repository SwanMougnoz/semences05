from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from s5vitrine.forms import ContactForm
from s5vitrine.models import Menuitem


class ContactView(TemplateView):

    template_name = "s5vitrine/contact.html"

    def get(self, request, *args, **kwargs):
        menuitem = Menuitem.objects.get(pk='contact')
        form = ContactForm()

        return self.render_to_response({
            "menu_actif": menuitem,
            "form": form
        })

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')
        return self.get(request)
