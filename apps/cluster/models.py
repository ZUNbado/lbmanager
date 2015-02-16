from django.db import models
from ..config.models import Server, Group

class ClusterDefaults(models.Model):
    enabled = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Member(ClusterDefaults):
    server = models.ForeignKey(Server)
    port = models.IntegerField(default=80)
    ssl_port = models.IntegerField(blank=True,null=True)

    def __unicode__(self):
        return u"%s / %s:%d" % (self.server.name, self.server.address, self.port)

    class Meta:
        verbose_name = 'Member'

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
    backends.verbose_name = 'Members'
    address = models.IPAddressField()
    port = models.IntegerField(default=80)
    port.verbose_name = 'Plain Port'
    ssl = models.BooleanField(default=False)
    ssl_port = models.IntegerField(default=443,blank=True,null=True)
    ssl_port.verbose_name = 'SSL Port'
    mode = models.CharField(
        max_length=4,
        choices=CLUSTER_MODES,
        default='gate',
    )
    fallback_ip = models.IPAddressField(blank=True,null=True, verbose_name=u"IP")
    fallback_ip.verbose_name = 'Fallback Address'
    fallback_port = models.IntegerField(blank=True,null=True, verbose_name=u"Port")
    fallback_port.verbose_name = 'Fallback Port'
    scheduler = models.CharField(
        max_length = 5,
        choices=SCHEDULER_MODES,
        default='wrr',
    )
    persistent = models.IntegerField(blank=True,null=True)
    netmask = models.IPAddressField(blank=True,null=True)
    protocol = models.CharField(
        max_length=3,
        choices=(
            ( 'tcp', 'TCP' ),
            ( 'udp', 'UDP' ),
        ),
        default='tcp',
        blank=True,null=True
    )

    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        verbose_name = 'Service IP Cluster'
