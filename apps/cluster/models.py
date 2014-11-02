from django.db import models

class ClusterDefaults(models.Model):
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Member(ClusterDefaults):
    name = models.CharField(max_length=200)
    address = models.IPAddressField()
    port = models.IntegerField(default=80)

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
    port = models.IntegerField(default=80)
    mode = models.CharField(
        max_length=4,
        choices=CLUSTER_MODES,
        default='gate',
    )
    fallback_ip = models.IPAddressField(blank=True,null=True)
    fallback_port = models.IntegerField(blank=True,null=True)
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
