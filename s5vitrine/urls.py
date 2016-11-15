from django.conf.urls import url
from s5vitrine import views

urlpatterns = [
    url(r'^$', views.AccueilView.as_view(), name='s5vitrine.accueil_view'),
    url(r'^contenus/(?P<contenu_id>[0-9]+)/$', views.ContenuView.as_view(), name='s5vitrine.contenu_view')
]
