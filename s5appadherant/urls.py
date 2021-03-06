from django.conf.urls import url

from s5appadherant.views import login, profil, variete, accueil, \
    jardin, culture, cultivateur, action

app_name = 's5appadherant'
urlpatterns = [
    url(r'^$', accueil.AccueilView.as_view(), name='accueil'),
    url(r'^login/$', login.LoginView.as_view(), name='login'),
    url(r'^logout/$', login.LogoutView.as_view(), name='logout'),

    url(r'^profil/$', profil.ProfilDetailView.as_view(), name='profil_current'),
    url(r'^profil/(?P<adherant_id>[0-9]+)/$', profil.ProfilDetailView.as_view(), name='profil_detail'),
    url(r'^profil/edit/$', profil.ProfilEditView.as_view(), name='profil_edit'),
    url(r'^profil/(?P<adherant_id>[0-9]+)/jardins/tabledata/$', profil.ProfilJardinDataView.as_view(), name='profil_jardin_data'),

    url(r'^varietes/$', variete.VarieteListView.as_view(), name='variete_list'),
    url(r'^varietes/(?P<variete_id>[0-9]+)/$', variete.VarieteDetailView.as_view(), name='variete_detail'),
    url(r'^varietes/new/$', variete.VarieteAddView.as_view(), name='variete_new'),
    url(r'^varietes/edit/(?P<pk>[0-9]+)/$', variete.VarieteEditView.as_view(), name='variete_edit'),

    url(r'^jardins/$', jardin.JardinListView.as_view(), name='jardin_all'),
    url(r'^jardins/adherant/(?P<adherant_id>[0-9]+)/$', jardin.JardinAdherantListView.as_view(), name='jardin_adherant'),
    url(r'^jardins/cultivateur/(?P<adherant_id>[0-9]+)/$', jardin.JardinCultivateurListView.as_view(), name='jardin_cultivateur'),
    url(r'^jardins/(?P<jardin_id>[0-9]+)/$', jardin.JardinDetailView.as_view(), name='jardin_detail'),
    url(r'^jardins/new/$', jardin.JardinAddView.as_view(), name='jardin_new'),
    url(r'^jardins/edit/(?P<jardin_id>[0-9]+)/$', jardin.JardinEditView.as_view(), name='jardin_edit'),

    url(r'^jardins/(?P<jardin_id>[0-9]+)/cultures/new/$', culture.CultureAddView.as_view(), name='culture_new'),
    url(r'^jardins/(?P<jardin_id>[0-9]+)/cultures/(?P<culture_id>[0-9]+)/delete/$', culture.CultureDeleteView.as_view(), name='culture_delete'),
    url(r'^jardins/(?P<jardin_id>[0-9]+)/cultures/tabledata/$', culture.CultureDataView.as_view(), name='culture_data'),

    url(r'^jardins/(?P<jardin_id>[0-9]+)/cultivateur/request/$', cultivateur.CultivateurRequestView.as_view(), name='cultivateur_request'),
    url(r'^jardins/(?P<jardin_id>[0-9]+)/cultivateur/confirmation/$', cultivateur.CultivateurConfirmationView.as_view(), name='cultivateur_confirmation'),
    url(r'^jardins/(?P<cultivateur_id>[0-9]+)/cultivateur/decide/$', cultivateur.CultivateurDecideView.as_view(), name='cultivateur_decide'),
    url(r'^jardins/(?P<jardin_id>[0-9]+)/cultivateurs/(?P<cultivateur_id>[0-9]+)/delete/$', cultivateur.CultivateurDeleteView.as_view(), name='cultivateur_delete'),
    url(r'^jardins/(?P<jardin_id>[0-9]+)/cultivateurs/(?P<cultivateur_id>[0-9]+)/quit/$', cultivateur.CultivateurQuitView.as_view(), name='cultivateur_quit'),

    url(r'action/(?P<action_id>[0-9]+)/process/$', action.ProcessActionView.as_view(), name='action_process')
]
