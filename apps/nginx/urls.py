from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^apply$', views.apply, name='apply'),
]
