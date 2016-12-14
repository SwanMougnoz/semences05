from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.core.mail import send_mail
from s5vitrine.forms.contact import ContactForm
from s5vitrine.models.menuitem import Menuitem


class ContactView(TemplateView):

    template_name = "s5vitrine/contact.html"

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

            destinataires = ['mougnoz.swan@gmail.com']
            if send_copy:
                destinataires.append(str(expediteur))

            # todo : activer en production
            # send_mail(objet, message, expediteur, destinataires)

            return redirect("s5vitrine:contact_envoye")

        return self.get(request, form=form)


class ContactEnvoyeView(TemplateView):

    template_name = 's5vitrine/contact_envoye.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
