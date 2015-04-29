from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^opinions/$', 'opinions.views.index', name='opinions'),
    url(r'^opinions/citations/(\d+)$', 'opinions.views.opinion_citations', name='opinion'),
]
