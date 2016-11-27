from django.conf.urls import url
from s5appadherant import views

app_name = 's5appadherant'
urlpatterns = [
    url(r'^$', views.AccueilView.as_view(), name='accueil_view'),
    url(r'^login/$', views.LoginView.as_view(), name='login_view'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout_view')
]
