from django.conf.urls import url
from s5appadherant import views

app_name = 's5appadherant'
urlpatterns = [
    url(r'^$', views.AccueilView.as_view(), name='accueil_view'),
    url(r'^login/$', views.LoginView.as_view(), name='login_view'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout_view'),
    url(r'^varietes/$', views.VarietelistView.as_view(), name='variete_list_view'),
    url(r'^varietes/(?P<variete_id>[0-9]+)/$', views.VarieteDetailView.as_view(), name='variete_detail_view'),
    url(r'^varietes/new/$', views.VarieteAddView.as_view(), name='variete_new_view'),
    url(r'^varietes/edit/(?P<pk>[0-9]+)$', views.VarieteEditView.as_view(), name='variete_edit_view')
]
