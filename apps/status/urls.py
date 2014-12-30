from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
        url(r'^show_image/(?P<graph>[a-zA-Z0-9]+)/(?P<end>[0-9]+)/(?P<start>[0-9]+)/$', views.show_image, name='show_image'),
]
