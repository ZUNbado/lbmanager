from django.db import models
from ..config.models import Server, Group

class BalancerDefaults(models.Model):
    enabled = models.BooleanField(default=True)
    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Backend(BalancerDefaults):
    name = models.CharField(max_length=200)
    server = models.ForeignKey(Server)
    port = models.IntegerField(default=80)
    host_header = models.CharField(max_length=200,null=True,blank=True)
    connect_timeout = models.IntegerField(null=True,blank=True)
    first_byte_timeout = models.IntegerField(null=True,blank=True)
    between_bytes_timeout = models.IntegerField(null=True,blank=True)
    max_connections = models.IntegerField(null=True,blank=True)
    probe_url = models.CharField(max_length=200,null=True,blank=True, verbose_name=u"URL")
    probe_timeout = models.IntegerField(null=True,blank=True, verbose_name=u"Timeout")
    probe_interval = models.IntegerField(null=True,blank=True, verbose_name=u"Interval")
    probe_window = models.IntegerField(null=True,blank=True, verbose_name=u"Window")
    probe_threshold = models.IntegerField(null=True,blank=True, verbose_name=u"Threshold")
   
class Director(BalancerDefaults):
    TYPES = (
        ( 'Random', (
            ( 'random', 'Random'),
            ( 'client', 'Client'),
            ( 'hash', 'Hash' ),
        ),
        ),
        ( 'round-robin', 'Round Robin' ),
        ( 'dns', 'DNS' ),
        ( 'fallback', 'Fallback' )
    )
    name = models.CharField(max_length=200)
    backends = models.ManyToManyField(Backend)
    dirtype = models.CharField(max_length=200,choices=TYPES,default='round-robin', verbose_name=u"Director type")
