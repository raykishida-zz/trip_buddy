from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.dashboard),
    url(r'^view/(?P<id>\d+)$', views.detail),
    url(r'^addtrip$', views.addtrip),
    url(r'^create$', views.create),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^cancel/(?P<id>\d+)$', views.cancel),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^logout$', views.logout)
]