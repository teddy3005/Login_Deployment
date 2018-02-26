from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^users$', views.createUser),
    url(r'^login$', views.login),
    url(r'^show$', views.view_result),
]