from django.db import models

class Server(models.Model):
    name = models.CharField(max_length=200)
    address = models.IPAddressField()
    ssh_user = models.CharField(max_length=200)
    ssh_password = models.CharField(max_length=200)
    ssh_port = models.IntegerField(default=22)
    enabled = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s" % self.name


class Group(models.Model):
    name = models.CharField(max_length=200)
    enabled = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s" % self.name


class Config(models.Model):
    group = models.OneToOneField(Group)
    temp_dir = models.CharField(max_length=200,default='/tmp/lbmanager')
    nginx_maps_dir = models.CharField(max_length=200)
    nginx_conf_dir = models.CharField(max_length=200)
    nginx_sites_dir = models.CharField(max_length=200)
    ldirectord_conf = models.CharField(max_length=200)
    varnish_dir = models.CharField(max_length=200)
    cluster_servers = models.ManyToManyField(Server)
    enable_transfer = models.BooleanField(default=True)
    enable_reload = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s" % (self.group.name)
