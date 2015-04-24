from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'scotus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'scotus.views.overview', name='overview'),
    url('', include('citations.urls')),
    url('', include('opinions.urls')),
    url('', include('justices.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
