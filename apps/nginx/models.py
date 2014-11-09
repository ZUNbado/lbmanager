from django.db import models
from ..config.models import Group
from ..cluster.models import Cluster
from ..balancer.models import Director

import base64, hashlib, os

class NginxDefaults(models.Model):
    enabled = models.BooleanField(default=True)
    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        abstract = True

# Clase per opcions de nginx, encara per definir
class HostConfig(NginxDefaults):
    group = models.ForeignKey(Group)

class AuthUser(NginxDefaults):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    encrypted = models.CharField(max_length=200,null=True,blank=True)

    def save(self, *args, **kwargs):
        salt = 'test'
        self.encrypted='{SSHA}' + base64.b64encode(hashlib.sha1(self.password + salt).digest() + salt)
        super(AuthUser, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = '3- Autenticate users'

class Location(NginxDefaults):
    TYPES = (
        ('proxy', 'Proxy'),
        ('files', 'Static'),
    )
    name = models.CharField(max_length=200)
    path_url = models.CharField(max_length=200)
    backend_type = models.CharField(max_length=5,choices=TYPES,default='proxy',null=True,blank=True)
    director = models.ForeignKey(Director,null=True,blank=True)
    path_fs = models.CharField(max_length=200,null=True,blank=True)
    auth_basic_enabled = models.BooleanField(default=False)
    auth_basic_msg = models.CharField(max_length=200,null=True,blank=True)
    users = models.ManyToManyField(AuthUser,null=True,blank=True)
    ip_allow_enabled = models.BooleanField(default=False)
    ip_allow_list = models.CharField(max_length=200,null=True,blank=True)

    class Meta:
        verbose_name_plural = '2- Location'

class NginxVirtualHost(NginxDefaults):
    REDIRECTS = (
        (301, 'Permanent'),
        (302, 'Temporal'),
    )
    name = models.CharField(max_length=200)
    cluster = models.ManyToManyField(Cluster)
    location = models.ManyToManyField(Location)
    extraconf = models.TextField(null=True,blank=True)
    access_log = models.CharField(max_length=200,null=True,blank=True)
    redirect_type = models.IntegerField(choices=REDIRECTS,default=301)
    ssl_cert = models.TextField(null=True,blank=True)
    ssl_key = models.TextField(null=True,blank=True)
    ssl_ca = models.TextField(null=True,blank=True)

    def get_clusters(self):
        return ", ".join([c.name for c in self.cluster.filter(enabled=True)])

    def get_locations(self):
        return ", ".join([l.name for l in self.location.filter(enabled=True)])

    def get_ssl(self):
        ssl=False
        for c in self.cluster.filter(enabled=True): 
            if c.ssl is True: 
                ssl=True
        return ssl
    get_ssl.boolean = True
    get_ssl.short_description = 'SSL Enabled'

    class Meta:
        verbose_name_plural = '1- VirtualHost'
