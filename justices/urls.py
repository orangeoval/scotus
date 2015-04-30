from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^justices/$', 'justices.views.index', name='justices'),
    url(r'^justices/opinions/(\w+)$', 'justices.views.justice_opinions', name='justice opinions'),
    url(r'^justices/opinions/citations/(\w+)$', 'justices.views.justice_opinions_citations', name='justice opinions citations'),
]
