# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
        ('cluster', '0002_cluster_ssl'),
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
                ('path', models.CharField(max_length=200)),
                ('auth_basic_enabled', models.BooleanField()),
                ('auth_basic_msg', models.CharField(max_length=200)),
                ('ip_allow_enabled', models.BooleanField()),
                ('ip_allow_list', models.CharField(max_length=200)),
                ('users', models.ManyToManyField(to='nginx.AuthUser')),
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
                ('ssl_cert', models.TextField(null=True, blank=True)),
                ('ssl_key', models.TextField(null=True, blank=True)),
                ('ssl_ca', models.TextField(null=True, blank=True)),
                ('cluster', models.ManyToManyField(to='cluster.Cluster')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VirtualHostTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(default=b'proxy', max_length=5, choices=[(b'proxy', b'Proxy'), (b'files', b'Static')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='nginxvirtualhost',
            name='template',
            field=models.ForeignKey(to='nginx.VirtualHostTemplate'),
            preserve_default=True,
        ),
    ]
