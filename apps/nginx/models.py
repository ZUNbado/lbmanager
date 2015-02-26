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

class AuthUser(NginxDefaults):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    encrypted = models.CharField(max_length=200,null=True,blank=True)

    def save(self, *args, **kwargs):
        salt = 'test'
        self.encrypted='{SSHA}' + base64.b64encode(hashlib.sha1(self.password + salt).digest() + salt)
        super(AuthUser, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'Web Auth Users'
        verbose_name = 'Web Auth User'

class Location(NginxDefaults):
    TYPES = (
        ('proxy', 'Proxy'),
        ('files', 'Static'),
    )
    name = models.CharField(max_length=200)
    name.verbose_name = 'Description'
    path_url = models.CharField(max_length=200)
    path_url.verbose_name = 'Path URL'
    nginx_virtualhost = models.ForeignKey('NginxVirtualHost')
    access_log = models.CharField(max_length=200,null=True,blank=True)
    backend_type = models.CharField(max_length=5,choices=TYPES,default='proxy',null=True,blank=True)
    backend_type.verbose_name = 'Backend Mode'
    director = models.ForeignKey(Director,null=True,blank=True)
    path_fs = models.CharField(max_length=200,null=True,blank=True)
    path_fs.verbose_name = 'Path FS'
    auth_basic_enabled = models.BooleanField(default=False)
    auth_basic_msg = models.CharField(max_length=200,null=True,blank=True)
    users = models.ManyToManyField(AuthUser,null=True,blank=True)
    ip_allow_enabled = models.BooleanField(default=False)
    ip_allow_enabled.verbose_name = 'Enabled IP Restriction'
    ip_allow_list = models.CharField(max_length=200,null=True,blank=True)
    ip_allow_list.verbose_name = 'Allowed list IP'

    class Meta:
        unique_together = ( ( 'path_url', 'nginx_virtualhost' ), )

class NginxVirtualHost(NginxDefaults):
    REDIRECTS = (
        (301, 'Permanent'),
        (302, 'Temporal'),
    )
    name = models.CharField(max_length=200)
    cluster = models.ManyToManyField(Cluster)
    extraconf = models.TextField(null=True,blank=True)
    extraconf.verbose_name = 'Extra Configuration'
    access_log = models.CharField(max_length=200,null=True,blank=True)
    redirect_type = models.IntegerField(choices=REDIRECTS,default=301,blank=True,null=True)
    redirect_type.verbose_name = 'Default redirect'
    ssl_cert = models.TextField(null=True,blank=True)
    ssl_cert.verbose_name = 'SSL Certificate'
    ssl_key = models.TextField(null=True,blank=True)
    ssl_key.verbose_name = 'SSL Key'
    ssl_ca = models.TextField(null=True,blank=True)
    ssl_ca.verbose_name = 'SSL CA'

    def save(self, *args, **kwargs):
        super(NginxVirtualHost, self).save(*args, **kwargs)
        try:
            (location, created) = Location.objects.get_or_create(path_url='/', nginx_virtualhost = self)
        except:
            created = False
        if created:
            location.name = 'Default'
            if self.access_log: location.access_log = self.access_log
            location.save()

    def get_clusters(self):
        return ", ".join([c.name for c in self.cluster.filter(enabled=True)])

    def get_locations(self):
        return ", ".join([l.name for l in Location.objects.filter(enabled=True, nginx_virtualhost=self)])

    def get_ssl(self):
        ssl=False
        for c in self.cluster.filter(enabled=True): 
            if c.ssl is True: 
                ssl=True
        return ssl
    get_ssl.boolean = True
    get_ssl.short_description = 'SSL Enabled'

    class Meta:
        verbose_name_plural = 'VirtualHost'
        verbose_name = 'VirtualHost'
