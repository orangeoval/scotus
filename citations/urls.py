from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^citations/$', 'citations.views.index', name='citations'),
    url(r'^citations/(\d+)$', 'citations.views.opinion_citations', name='opinion citations'),
    url(r'^citations/(\w+)$', 'citations.views.justice_opinions_citations', name='justice opinions citations'),
]
