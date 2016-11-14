from django.conf.urls import url
from s5vitrine import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='s5vitrine.home_view'),
    url(r'^contenus/(?P<content_id>[0-9]+)/$', views.ContentView.as_view(), name='s5vitrine.content_view')
]
