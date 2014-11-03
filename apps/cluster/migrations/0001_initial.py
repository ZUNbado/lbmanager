# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('address', models.IPAddressField()),
                ('port', models.IntegerField(default=80)),
                ('mode', models.CharField(default=b'gate', max_length=4, choices=[(b'gate', b'Direct'), (b'ipip', b'Tunel IPIP'), (b'masq', b'Masquerading')])),
                ('fallback_ip', models.IPAddressField(null=True, blank=True)),
                ('fallback_port', models.IntegerField(null=True, blank=True)),
                ('scheduler', models.CharField(default=b'wrr', max_length=5, choices=[(b'rr', b'Robin Robin'), (b'wrr', b'Weighted  Round  Robin'), (b'lc', b'Least-Connection'), (b'wlc', b'Weighted  Least-Connection'), (b'lblc', b'Locality-Based  Least-Connection'), (b'lblcr', b'Locality-Based  Least-Connection   with   Replication'), (b'dh', b'Destination  Hashing'), (b'sh', b'Source Hashing'), (b'sed', b'Shortest Expected Delay'), (b'nq', b'Never Queue')])),
                ('persistent', models.IntegerField(default=300)),
                ('netmask', models.IPAddressField(null=True, blank=True)),
                ('protocol', models.CharField(default=b'tcp', max_length=3, choices=[(b'tcp', b'TCP'), (b'udp', b'UDP')])),
            ],
            options={
                'verbose_name_plural': '2- Cluster',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('port', models.IntegerField(default=80)),
                ('server', models.ForeignKey(to='config.Server')),
            ],
            options={
                'verbose_name_plural': '1- Member',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cluster',
            name='backends',
            field=models.ManyToManyField(to='cluster.Member'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cluster',
            name='group',
            field=models.ForeignKey(to='config.Group'),
            preserve_default=True,
        ),
    ]