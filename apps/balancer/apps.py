from django.apps import AppConfig
from django.apps import apps as django_apps

class BalancerConfig(AppConfig):
    name = "apps.balancer"
    verbose_name = "3- Load Balancer"
