from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^users$', views.createUser),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^show$', views.view_result),
    url(r'^addplan$', views.addplan),
    url(r'^createplan$', views.createplan),
    url(r'^show/(?P<travel_id>\d+)$', views.show),
    url(r'^join/(?P<travel_id>\d+)$', views.join),
    url(r'^delete/(?P<id>\d+)$', views.delete)
    
    
]