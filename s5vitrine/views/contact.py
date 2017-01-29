from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.core.mail import send_mail
from s5vitrine.forms.contact import ContactForm
from s5vitrine.models.menuitem import Menuitem


class ContactView(TemplateView):

    template_name = "s5vitrine/contact/form.html"

    def get(self, request, *args, **kwargs):
        menuitem = Menuitem.objects.get(pk='contact')
        form = kwargs.get('form', ContactForm())

        return self.render_to_response({
            "menu_actif": menuitem,
            "form": form
        })

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            expediteur = form.cleaned_data['email']
            objet = form.cleaned_data['objet']
            message = form.cleaned_data['message']
            send_copy = form.cleaned_data['send_copy']

            destinataires = [settings.CONTACT_EMAIL]
            if send_copy:
                destinataires.append(str(expediteur))

            send_mail(objet, message, settings.DEFAULT_FROM_EMAIL, destinataires)

            return redirect("s5vitrine:contact_envoye")

        return self.get(request, form=form)


class ContactEnvoyeView(TemplateView):

    template_name = 's5vitrine/contact/envoye.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
