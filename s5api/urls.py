from django.conf.urls import url, include

from s5api import views

map_patterns = [
    url(r'^jardins/$', views.MapJardinListView.as_view(), name='map_jardin_list'),
    url(r'^jardins/(?P<pk>[0-9]+)/$', views.MapJardinDetailView.as_view(), name='map_jardin_detail'),
    url(r'^jardins/(?P<pk>[0-9]+)/cultures/$', views.MapCultureListView.as_view(), name='map_culture_list')
]

app_name = 's5api'
urlpatterns = [
    url(r'^map/', include(map_patterns))
]
