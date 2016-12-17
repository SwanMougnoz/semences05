from django.conf.urls import url
from s5appadherant.views import login, variete, accueil, jardin

app_name = 's5appadherant'
urlpatterns = [
    url(r'^$', accueil.AccueilView.as_view(), name='accueil'),
    url(r'^login/$', login.LoginView.as_view(), name='login'),
    url(r'^logout/$', login.LogoutView.as_view(), name='logout'),
    url(r'^varietes/$', variete.VarieteListView.as_view(), name='variete_list'),
    url(r'^varietes/(?P<variete_id>[0-9]+)/$', variete.VarieteDetailView.as_view(), name='variete_detail'),
    url(r'^varietes/new/$', variete.VarieteAddView.as_view(), name='variete_new'),
    url(r'^varietes/edit/(?P<pk>[0-9]+)$', variete.VarieteEditView.as_view(), name='variete_edit'),
    url(r'^jardins/$', jardin.JardinListView.as_view(), name='jardin_list'),
    url(r'^jardins/(?P<jardin_id>[0-9]+)/$', jardin.JardinDetailView.as_view(), name='jardin_detail'),
    url(r'^jardins/new/$', jardin.JardinAddView.as_view(), name='jardin_new')
]
