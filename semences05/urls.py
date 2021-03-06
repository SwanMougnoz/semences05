import debug_toolbar
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django_js_reverse.views import urls_js

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('s5vitrine.urls')),
    url(r'^adherant/', include('s5appadherant.urls')),
    url(r'^api/', include('s5api.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^activity/', include('actstream.urls')),
    url(r'^jsreverse/$', urls_js, name='js_reverse'),
    url(r'^__debug__/', include(debug_toolbar.urls))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
