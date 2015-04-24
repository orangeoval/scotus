from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'scotus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'scotus.views.overview', name='overview'),
    url(r'^admin/', include(admin.site.urls)),
]
