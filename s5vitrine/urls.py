from django.conf.urls import url
from s5vitrine.views import accueil, contact, contenu, variete

app_name = 's5vitrine'
urlpatterns = [
    url(r'^$', accueil.AccueilView.as_view(), name='accueil'),
    url(r'^contact/$', contact.ContactView.as_view(), name='contact'),
    url(r'^contact/envoye/$', contact.ContactEnvoyeView.as_view(), name='contact_envoye'),
    url(r'^contenus/(?P<contenu_id>[0-9]+)/$', contenu.ContenuView.as_view(), name='contenu'),
    url(r'^varietes/$', variete.VarieteListView.as_view(), name='variete_list'),
    url(r'^varietes/(?P<variete_id>[0-9]+)/$', variete.VarieteDetailView.as_view(), name='variete_detail')
]
