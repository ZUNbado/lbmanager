# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('balancer', '0001_initial'),
        ('config', '0001_initial'),
        ('cluster', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HostConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('group', models.ForeignKey(to='config.Group')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('path_url', models.CharField(max_length=200)),
                ('backend_type', models.CharField(default=b'proxy', max_length=5, choices=[(b'proxy', b'Proxy'), (b'files', b'Static')])),
                ('path_fs', models.CharField(max_length=200, null=True, blank=True)),
                ('auth_basic_enabled', models.BooleanField(default=False)),
                ('auth_basic_msg', models.CharField(max_length=200, null=True, blank=True)),
                ('ip_allow_enabled', models.BooleanField(default=False)),
                ('ip_allow_list', models.CharField(max_length=200, null=True, blank=True)),
                ('director', models.ForeignKey(blank=True, to='balancer.Director', null=True)),
                ('users', models.ManyToManyField(to='nginx.AuthUser', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NginxVirtualHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('extraconf', models.TextField(null=True, blank=True)),
                ('access_log', models.CharField(max_length=200, null=True, blank=True)),
                ('redirect_type', models.IntegerField(default=301, choices=[(301, b'Permanent'), (302, b'Temporal')])),
                ('ssl_cert', models.TextField(null=True, blank=True)),
                ('ssl_key', models.TextField(null=True, blank=True)),
                ('ssl_ca', models.TextField(null=True, blank=True)),
                ('cluster', models.ManyToManyField(to='cluster.Cluster')),
                ('location', models.ManyToManyField(to='nginx.Location')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
