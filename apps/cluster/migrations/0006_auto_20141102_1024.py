# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0005_auto_20141030_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='cluster',
            name='fallback_ip',
            field=models.IPAddressField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cluster',
            name='fallback_port',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cluster',
            name='mode',
            field=models.CharField(default=b'gate', max_length=4, choices=[(b'gate', b'Direct'), (b'ipip', b'Tunel IPIP'), (b'masq', b'Masquerading')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cluster',
            name='netmask',
            field=models.IPAddressField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cluster',
            name='persistent',
            field=models.IntegerField(default=300),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cluster',
            name='port',
            field=models.IntegerField(default=80),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cluster',
            name='protocol',
            field=models.CharField(default=b'tcp', max_length=3, choices=[(b'tcp', b'TCP'), (b'udp', b'UDP')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cluster',
            name='scheduler',
            field=models.CharField(default=b'wrr', max_length=5, choices=[(b'rr', b'Robin Robin'), (b'wrr', b'Weighted  Round  Robin'), (b'lc', b'Least-Connection'), (b'wlc', b'Weighted  Least-Connection'), (b'lblc', b'Locality-Based  Least-Connection'), (b'lblcr', b'Locality-Based  Least-Connection   with   Replication'), (b'dh', b'Destination  Hashing'), (b'sh', b'Source Hashing'), (b'sed', b'Shortest Expected Delay'), (b'nq', b'Never Queue')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='port',
            field=models.IntegerField(default=80),
            preserve_default=True,
        ),
    ]
