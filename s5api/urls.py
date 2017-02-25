from django.conf.urls import url, include

from s5api.views import MapJardinListView, MapJardinDetailView

map_patterns = [
    url(r'^jardins/$', MapJardinListView.as_view(), name='map_jardin_list'),
    url(r'^jardins/(?P<pk>[0-9]+)/$', MapJardinDetailView.as_view(), name='map_jardin_detail')
]

app_name = 's5api'
urlpatterns = [
    url(r'^map/', include(map_patterns))
]
