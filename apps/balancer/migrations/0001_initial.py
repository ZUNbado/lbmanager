# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Backend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('port', models.IntegerField(default=80)),
                ('host_header', models.CharField(max_length=200, null=True, blank=True)),
                ('connect_timeout', models.IntegerField(null=True, blank=True)),
                ('first_byte_timeout', models.IntegerField(null=True, blank=True)),
                ('between_bytes_timeout', models.IntegerField(null=True, blank=True)),
                ('max_connections', models.IntegerField(null=True, blank=True)),
                ('probe_url', models.CharField(max_length=200, null=True, verbose_name='URL', blank=True)),
                ('probe_timeout', models.IntegerField(null=True, verbose_name='Timeout', blank=True)),
                ('probe_interval', models.IntegerField(null=True, verbose_name='Interval', blank=True)),
                ('probe_window', models.IntegerField(null=True, verbose_name='Window', blank=True)),
                ('probe_threshold', models.IntegerField(null=True, verbose_name='Threshold', blank=True)),
                ('server', models.ForeignKey(to='config.Server')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('dirtype', models.CharField(default=b'round-robin', max_length=200, verbose_name='Director type', choices=[(b'Random', ((b'random', b'Random'), (b'client', b'Client'), (b'hash', b'Hash'))), (b'round-robin', b'Round Robin'), (b'dns', b'DNS'), (b'fallback', b'Fallback')])),
                ('backends', models.ManyToManyField(to='balancer.Backend')),
                ('group', models.ForeignKey(to='config.Group')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
