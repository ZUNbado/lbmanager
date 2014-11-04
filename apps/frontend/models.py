from django.db import models
from ..balancer.models import Director
from ..cluster.models import Cluster

class FrontendDefaults(models.Model):
    enabled = models.BooleanField(default=True)
    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Domain(FrontendDefaults):
    name = models.CharField(max_length=200)
    director = models.ForeignKey(Director)
    cache = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "3- Domain"

class DomainAlias(FrontendDefaults):
    name = models.CharField(max_length=200)
    domain = models.ForeignKey(Domain)

    def alias(self):
        return self.name

    alias.short_description = 'Domain Alias'

    class Meta:
        verbose_name_plural = "4- Domain Alias"

class VirtualHostType(FrontendDefaults):
    name = models.CharField(max_length=200)
    template = models.TextField()

    class Meta:
        verbose_name_plural = "2- Virtual Host Template"

class VirtualHost(FrontendDefaults):
    name = models.CharField(max_length=200)
    clusters = models.ManyToManyField(Cluster)
    virtualhosttype = models.ForeignKey(VirtualHostType, verbose_name=u"Template")
    extraconf = models.TextField(null=True,blank=True)
    access_log = models.CharField(max_length=200,null=True,blank=True)
    ssl_cert = models.TextField(null=True,blank=True)
    ssl_key = models.TextField(null=True,blank=True)
    ssl_ca = models.TextField(null=True,blank=True)

    class Meta:
        verbose_name_plural = "1- Virtual Host"

class HostRedir(FrontendDefaults):
    name = models.CharField(max_length=200)
    domain = models.ForeignKey(Domain)
    
    class Meta:
        verbose_name_plural = "5- Host Redir"

class UrlRedir(FrontendDefaults):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "6- URL Redir"
