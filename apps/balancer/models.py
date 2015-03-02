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
#    host_header = models.CharField(max_length=200,null=True,blank=True)
    connect_timeout = models.IntegerField(null=True,blank=True)
    first_byte_timeout = models.IntegerField(null=True,blank=True)
    between_bytes_timeout = models.IntegerField(null=True,blank=True)
    max_connections = models.IntegerField(null=True,blank=True)
    probe_url = models.CharField(max_length=200,null=True,blank=True, verbose_name=u"URL")
    probe_timeout = models.IntegerField(null=True,blank=True, verbose_name=u"Timeout")
    probe_interval = models.IntegerField(null=True,blank=True, verbose_name=u"Interval")
    probe_window = models.IntegerField(null=True,blank=True, verbose_name=u"Window")
    probe_threshold = models.IntegerField(null=True,blank=True, verbose_name=u"Threshold")

    class Meta:
        verbose_name = 'Backend'
        unique_together = ( ( 'server', 'port'), )
   
class Director(BalancerDefaults):
    TYPES = (
        ( 'Random', (
            ( 'random', 'Random'),
            ( 'client', 'By Client'),
            ( 'hash', 'By Hash' ),
        ),
        ),
        ( 'round-robin', 'Round Robin' ),
#        ( 'dns', 'DNS' ),
        ( 'fallback', 'Fallback' )
    )

    TYPES_NGINX = (
            ( 'round-robin', 'Round Robibn' ),
            ( 'least_conn', 'Least Connected' ),
            ( 'ip_hash', 'Session persistance' ),
            ( 'weight', 'Weighted Round Robin' ),
            )
    name = models.CharField(max_length=200)
#    backends = models.ManyToManyField(Backend)
    backends_weight = models.ManyToManyField(Backend, through='DirectorBackendWeight', related_name='BackendWeight')
    dirtype = models.CharField(max_length=200,choices=TYPES,default='round-robin', verbose_name=u"Cache: Director type")
    dirtype_nginx = models.CharField(max_length=20,choices=TYPES_NGINX,default='round-robin', verbose_name=u'Front: Director type')

    class Meta:
        verbose_name = 'Director'

class DirectorBackendWeight(BalancerDefaults):
    backend = models.ForeignKey(Backend)
    director = models.ForeignKey(Director)
    weight = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '%s / %s' % (self.director.name, self.backend.name)

    class Meta:
        unique_together = ( ('backend', 'director') )
