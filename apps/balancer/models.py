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
    group = models.ForeignKey(Group)
    dirtype = models.CharField(max_length=200,choices=TYPES,default='round-robin')
