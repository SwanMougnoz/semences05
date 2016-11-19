from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('s5vitrine.urls')),
    url(r'^adherant/', include('s5appadherant.urls')),
]

urlpatterns += staticfiles_urlpatterns()
