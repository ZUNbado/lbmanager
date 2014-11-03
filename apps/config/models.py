from django.db import models

class ConfigDefaultAdmin(models.Model):
    enabled = models.BooleanField(default=True)
    def __unicode__(self):
        return u"%s" % self.name

class Server(ConfigDefaultAdmin):
    name = models.CharField(max_length=200)
    address = models.IPAddressField()
    ssh_user = models.CharField(max_length=200)
    ssh_password = models.CharField(max_length=200)
    ssh_port = models.IntegerField(default=22)

class Group(ConfigDefaultAdmin):
    name = models.CharField(max_length=200)

class Config(ConfigDefaultAdmin):
    group = models.OneToOneField(Group)
    temp_dir = models.CharField(max_length=200)
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

    def enable_link(self):
        return '<a href="/admin/config/config/enable/%d/" class="link">Enable</a>' % self.id

    enable_link.short_description = 'Enable link'
    enable_link.allow_tags = True
