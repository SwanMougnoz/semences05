from django.conf.urls import url
from s5appadherant import views

urlpatterns = [
    url(r'^$', views.AccueilView.as_view(), name='s5appadherant.accueil_view'),
    url(r'^login/$', views.LoginView.as_view(), name='s5appadherant.login_view'),
    url(r'^logout/$', views.LogoutView.as_view(), name='s5appadherant.logout_view')
]
