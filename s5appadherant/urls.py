from django.conf.urls import url
from s5appadherant import views

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='s5appadherant.login_view')
]
