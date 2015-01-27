from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^sync$', views.sync, name='sync'),
	url(r'^health$', views.health, name='health'),
]
