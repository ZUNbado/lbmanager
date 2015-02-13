# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('balancer', '0001_initial'),
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
                ('encrypted', models.CharField(max_length=200, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Web Auth User',
                'verbose_name_plural': 'Web Auth Users',
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
                ('access_log', models.CharField(max_length=200, null=True, blank=True)),
                ('backend_type', models.CharField(default=b'proxy', max_length=5, null=True, blank=True, choices=[(b'proxy', b'Proxy'), (b'files', b'Static')])),
                ('path_fs', models.CharField(max_length=200, null=True, blank=True)),
                ('auth_basic_enabled', models.BooleanField(default=False)),
                ('auth_basic_msg', models.CharField(max_length=200, null=True, blank=True)),
                ('ip_allow_enabled', models.BooleanField(default=False)),
                ('ip_allow_list', models.CharField(max_length=200, null=True, blank=True)),
                ('director', models.ForeignKey(blank=True, to='balancer.Director', null=True)),
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
                ('redirect_type', models.IntegerField(default=301, null=True, blank=True, choices=[(301, b'Permanent'), (302, b'Temporal')])),
                ('ssl_cert', models.TextField(null=True, blank=True)),
                ('ssl_key', models.TextField(null=True, blank=True)),
                ('ssl_ca', models.TextField(null=True, blank=True)),
                ('cluster', models.ManyToManyField(to='cluster.Cluster')),
            ],
            options={
                'verbose_name': 'VirtualHost',
                'verbose_name_plural': 'VirtualHost',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='location',
            name='nginx_virtualhost',
            field=models.ForeignKey(to='nginx.NginxVirtualHost'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='users',
            field=models.ManyToManyField(to='nginx.AuthUser', null=True, blank=True),
            preserve_default=True,
        ),
    ]
