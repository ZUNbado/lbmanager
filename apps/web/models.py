from django.db import models
from ..balancer.models import Director
from ..cluster.models import Cluster
from ..nginx.models import NginxVirtualHost

class WebDefaults(models.Model):
    enabled = models.BooleanField(default=True)
    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Domain(WebDefaults):
    name = models.CharField(max_length=200)
    virtual_host = models.ForeignKey(NginxVirtualHost)
    director = models.ForeignKey(Director)
    cache = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "1- Domain"

class DomainAlias(WebDefaults):
    name = models.CharField(max_length=200)
    domain = models.ForeignKey(Domain)

    def alias(self):
        return self.name

    alias.short_description = 'Domain Alias'

    class Meta:
        verbose_name_plural = "2- Domain Alias"

class HostRedir(WebDefaults):
    name = models.CharField(max_length=200)
    domain = models.ForeignKey(Domain)
    
    class Meta:
        verbose_name_plural = "3- Host Redir"

class UrlRedir(WebDefaults):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    virtual_host = models.ForeignKey(NginxVirtualHost)

    class Meta:
        verbose_name_plural = "4- URL Redir"
