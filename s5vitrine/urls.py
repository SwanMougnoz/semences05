from django.conf.urls import url
from s5vitrine import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view()),
]
