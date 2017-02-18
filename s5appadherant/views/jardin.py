# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from rules.contrib.views import PermissionRequiredMixin

from s5appadherant.forms.adresse import AdresseFullForm
from s5appadherant.forms.jardin import JardinForm
from s5appadherant.models import Jardin, Adherant
from s5appadherant.tables.culture import CultureTableCultivateur, CultureTable
from s5appadherant import permissions


class JardinListView(LoginRequiredMixin, ListView):
    template_name = 's5appadherant/jardin/list.html'
    model = Jardin
    paginate_by = 10
    list_identifier = 'all'

    def get_context_data(self, **kwargs):
        context = super(JardinListView, self).get_context_data(**kwargs)
        context.update({
            'jardins': context.get('page_obj'),
            'list': self.list_identifier,
            'menu_actif': 'jardin',
            'titre_page': u"Mes jardins"
        })
        return context


class JardinAdherantListView(JardinListView):
    list_identifier = 'adherant'

    def get_queryset(self):
        adherant = get_object_or_404(Adherant, pk=self.kwargs.get('adherant_id'))
        return Jardin.objects.filter(proprietaire=adherant)


class JardinCultivateurListView(JardinListView):
    list_identifier = 'cultivateur'

    def get_queryset(self):
        adherant = get_object_or_404(Adherant, pk=self.kwargs.get('adherant_id'))
        return Jardin.objects.filter(cultivateur__accepte=True, cultivateur__adherant=adherant)


class JardinDetailView(LoginRequiredMixin, TemplateView):
    template_name = 's5appadherant/jardin/detail.html'

    def get(self, request, *args, **kwargs):
        jardin = get_object_or_404(Jardin, pk=kwargs.get('jardin_id'))

        if request.user.has_perm('s5appadherant.change_jardin', jardin):
            culture_table = CultureTableCultivateur(jardin=jardin)
        else:
            culture_table = CultureTable(jardin=jardin)

        qs = jardin.cultivateur_set.all()

        cultivateur_request_pending = request.user.adherant in \
            [cultivateur.adherant for cultivateur in qs.filter(pending=True)]

        cultivateurs_acceptes = qs.filter(accepte=True)

        return self.render_to_response({
            'jardin': jardin,
            'culture_table': culture_table,
            'cultivateur_request_pending': cultivateur_request_pending,
            'cultivateurs_acceptes': cultivateurs_acceptes,
            'menu_actif': 'jardin',
            'titre_page': u'Jardin - %s' % jardin.appelation
        })


class JardinAddView(LoginRequiredMixin, TemplateView):
    template_name = 's5appadherant/jardin/edit.html'

    def get(self, request, *args, **kwargs):
        jardin_form = kwargs.get('jardin_form', JardinForm())
        adresse_form = kwargs.get('adresse_form', AdresseFullForm())

        return self.render_to_response({
            'jardin_form': jardin_form,
            'adresse_form': adresse_form,
            'menu_actif': 'jardin',
            'titre_page': u"Ajout d'un jardin"
        })

    def post(self, request):
        jardin_form = JardinForm(request.POST)
        adresse_form = AdresseFullForm(request.POST)

        if jardin_form.is_valid() and adresse_form.is_valid():
            adresse = adresse_form.save()
            jardin = jardin_form.save(commit=False)
            jardin.adresse = adresse
            jardin.proprietaire = request.user.adherant
            jardin.save()

            return redirect('s5appadherant:jardin_detail', jardin_id=jardin.id)

        return self.get(request, jardin_form=jardin_form, adresse_form=adresse_form)


class JardinEditView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 's5appadherant/jardin/edit.html'
    permission_required = 's5appadherant.change_jardin'

    def get_permission_object(self):
        return get_object_or_404(Jardin, pk=self.kwargs.get('jardin_id'))

    def get(self, request, *args, **kwargs):
        jardin = get_object_or_404(Jardin, pk=kwargs.get('jardin_id'))

        jardin_form = kwargs.get('jardin_form', JardinForm(instance=jardin))
        adresse_form = kwargs.get('adresse_form', AdresseFullForm(instance=jardin.adresse))

        return self.render_to_response({
            'jardin': jardin,
            'jardin_form': jardin_form,
            'adresse_form': adresse_form,
            'menu_actif': 'jardin',
            'titre_page': u"Ajout d'un jardin"
        })

    def post(self, request, **kwargs):
        jardin = get_object_or_404(Jardin, pk=kwargs.get('jardin_id'))

        jardin_form = JardinForm(request.POST, instance=jardin)
        adresse_form = AdresseFullForm(request.POST, instance=jardin.adresse)

        if jardin_form.is_valid() and adresse_form.is_valid():
            adresse_form.save()
            jardin_form.save()

            return redirect('s5appadherant:jardin_detail', jardin_id=jardin.id)

        return self.get(request, jardin_id=jardin.id, jardin_form=jardin_form,
                        adresse_form=adresse_form)
