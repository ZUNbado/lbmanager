from django.db import models
from ..config.models import Server, Group

class ClusterDefaults(models.Model):
    enabled = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Member(ClusterDefaults):
    server = models.ForeignKey(Server)
    port = models.IntegerField(default=80)

    def __unicode__(self):
        return u"%s / %s:%d" % (self.server.name, self.server.address, self.port)

    class Meta:
        verbose_name_plural = "1- Member"


class Cluster(ClusterDefaults):
    CLUSTER_MODES = (
        ( 'gate', 'Direct' ),
        ( 'ipip', 'Tunel IPIP' ),
        ( 'masq', 'Masquerading' ),
    )

    SCHEDULER_MODES = (
        ( 'rr', 'Robin Robin'),
        ( 'wrr', 'Weighted  Round  Robin'),
        ( 'lc', 'Least-Connection' ),
        ( 'wlc', 'Weighted  Least-Connection' ),
        ( 'lblc', 'Locality-Based  Least-Connection' ),
        ( 'lblcr', 'Locality-Based  Least-Connection   with   Replication' ),
        ( 'dh', 'Destination  Hashing' ),
        ( 'sh', 'Source Hashing' ),
        ( 'sed', 'Shortest Expected Delay' ),
        ( 'nq', 'Never Queue'),
    )
    name = models.CharField(max_length=200)
    backends = models.ManyToManyField(Member)
    group = models.ForeignKey(Group)
    address = models.IPAddressField()
    port = models.IntegerField(default=80)
    mode = models.CharField(
        max_length=4,
        choices=CLUSTER_MODES,
        default='gate',
    )
    fallback_ip = models.IPAddressField(blank=True,null=True, verbose_name=u"IP")
    fallback_port = models.IntegerField(blank=True,null=True, verbose_name=u"Port")
    scheduler = models.CharField(
        max_length = 5,
        choices=SCHEDULER_MODES,
        default='wrr',
    )
    persistent = models.IntegerField(default=300)
    netmask = models.IPAddressField(blank=True,null=True)
    protocol = models.CharField(
        max_length=3,
        choices=(
            ( 'tcp', 'TCP' ),
            ( 'udp', 'UDP' ),
        ),
        default='tcp',
    )

    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        verbose_name_plural = "2- Cluster"
