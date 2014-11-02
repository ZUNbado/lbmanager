from django.apps import AppConfig
from django.apps import apps as django_apps

class ClusterConfig(AppConfig):
    name = "apps.cluster"
    verbose_name = "1- Cluster"
