from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^users$', views.createUser),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^show$', views.dashboard),
    url(r'^add$', views.add),
    url(r'^destroy/(?P<id>\d+)$', views.destroy),
    url(r'^edit$', views.edit),
    url(r'^create(?P<id>\d+)$', views.edit),
    url(r'^update/(?P<id>\d+)$', views.update),
    ]