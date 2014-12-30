from django.db import models

class ConfigDefaultAdmin(models.Model):
    enabled = models.BooleanField(default=True)
    def __unicode__(self):
        return u"%s" % self.name

class Server(ConfigDefaultAdmin):
    name = models.CharField(max_length=200)
    address = models.IPAddressField()
    ssh_user = models.CharField(max_length=200,null=True,blank=True)
    ssh_password = models.CharField(max_length=200,null=True,blank=True)
    ssh_port = models.IntegerField(default=22,null=True,blank=True)

    class Meta:
        verbose_name_plural = '2- Server'

class Group(ConfigDefaultAdmin):
    name = models.CharField(max_length=200)
    temp_dir = models.CharField(max_length=200)
    nginx_dir = models.CharField(max_length=200)
    ldirectord_conf = models.CharField(max_length=200)
    graph_dir = models.CharField(max_length=200)
    varnish_dir = models.CharField(max_length=200)
    cluster_servers = models.ManyToManyField(Server,null=True,blank=True)
    admin_port = models.IntegerField(default=8000,null=True,blank=True)
    enable_transfer = models.BooleanField(default=True)
    enable_reload = models.BooleanField(default=True)

    def __unicode__(self):
        return u"%s" % (self.group.name)

    class Meta:
        verbose_name_plural = '1- Group configuration'
