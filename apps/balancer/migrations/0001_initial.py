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
                ('dirtype', models.CharField(default=b'round-robin', max_length=200, choices=[(b'Random', ((b'random', b'Random'), (b'client', b'Client'), (b'hash', b'Hash'))), (b'round-robin', b'Round Robin'), (b'dns', b'DNS'), (b'fallback', b'Fallback')])),
                ('backends', models.ManyToManyField(to='balancer.Backend')),
                ('group', models.ForeignKey(to='config.Group')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
