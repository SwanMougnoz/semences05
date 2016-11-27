from django.conf.urls import url
from s5vitrine import views

app_name = 's5vitrine'
urlpatterns = [
    url(r'^$', views.AccueilView.as_view(), name='accueil_view'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact_view'),
    url(r'^contact/envoye/$', views.ContactEnvoyeView.as_view(), name='contact_envoye_view'),
    url(r'^contenus/(?P<contenu_id>[0-9]+)/$', views.ContenuView.as_view(), name='contenu_view'),
    url(r'^varietes/$', views.VarieteListView.as_view(), name='variete_list_view')
]
