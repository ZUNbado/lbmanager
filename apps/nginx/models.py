from django.db import models
from ..config.models import Group
from ..cluster.models import Cluster

class NginxDefaults(models.Model):
    enabled = models.BooleanField(default=True)
    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        abstract = True

# Clase per opcions de nginx, encara per definir
class HostConfig(NginxDefaults):
    group = models.ForeignKey(Group)
    

class VirtualHostTemplate(NginxDefaults):
    TYPES = (
        ('proxy', 'Proxy'),
        ('files', 'Static'),
    )
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=5,choices=TYPES,default='proxy')

class NginxVirtualHost(NginxDefaults):
    name = models.CharField(max_length=200)
    template = models.ForeignKey(VirtualHostTemplate)
    cluster = models.ManyToManyField(Cluster)
    extraconf = models.TextField(null=True,blank=True)
    access_log = models.CharField(max_length=200,null=True,blank=True)
    ssl_cert = models.TextField(null=True,blank=True)
    ssl_key = models.TextField(null=True,blank=True)
    ssl_ca = models.TextField(null=True,blank=True)


class AuthUser(NginxDefaults):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

class Location(NginxDefaults):
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    auth_basic_enabled = models.BooleanField(default=False)
    auth_basic_msg = models.CharField(max_length=200,null=True,blank=True)
    users = models.ManyToManyField(AuthUser,null=True,blank=True)
    ip_allow_enabled = models.BooleanField(default=False)
    ip_allow_list = models.CharField(max_length=200,null=True,blank=True)
