"""ResistenciaCoC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from ResistenciaCoC import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', views.index),
    url(r'^accounts/login/$', views.index),
    url(r'^logout/', views.user_logout),
    url(r'^registration/', views.registration),
    url(r'^index_logged_in/', views.index_logged_in),
    url(r'^create_clan/', views.create_clan),
    url(r'^join_clan/', views.join_clan),
    url(r'^clan/$', views.clan),


]
