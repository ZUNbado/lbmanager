from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/web/custom/', include('apps.web.urls')),
    url(r'^admin/balancer/custom/', include('apps.balancer.urls')),
    url(r'^admin/cluster/custom/', include('apps.cluster.urls')),
    url(r'^admin/nginx/custom/', include('apps.nginx.urls')),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

