from django.conf.urls import url
from s5appadherant.views import login, variete, accueil

app_name = 's5appadherant'
urlpatterns = [
    url(r'^$', accueil.AccueilView.as_view(), name='accueil_view'),
    url(r'^login/$', login.LoginView.as_view(), name='login_view'),
    url(r'^logout/$', login.LogoutView.as_view(), name='logout_view'),
    url(r'^varietes/$', variete.VarieteListView.as_view(), name='variete_list_view'),
    url(r'^varietes/(?P<variete_id>[0-9]+)/$', variete.VarieteDetailView.as_view(), name='variete_detail_view'),
    url(r'^varietes/new/$', variete.VarieteAddView.as_view(), name='variete_new_view'),
    url(r'^varietes/edit/(?P<pk>[0-9]+)$', variete.VarieteEditView.as_view(), name='variete_edit_view')
]
