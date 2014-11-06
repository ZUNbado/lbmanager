# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('balancer', '0001_initial'),
        ('nginx', '0001_initial'),
        ('cluster', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('cache', models.BooleanField(default=True)),
                ('director', models.ForeignKey(to='balancer.Director')),
                ('virtual_host', models.ForeignKey(to='nginx.NginxVirtualHost')),
            ],
            options={
                'verbose_name_plural': '3- Domain',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DomainAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('domain', models.ForeignKey(to='web.Domain')),
            ],
            options={
                'verbose_name_plural': '4- Domain Alias',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HostRedir',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('domain', models.ForeignKey(to='web.Domain')),
            ],
            options={
                'verbose_name_plural': '5- Host Redir',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UrlRedir',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('virtual_host', models.ForeignKey(to='nginx.NginxVirtualHost')),
            ],
            options={
                'verbose_name_plural': '6- URL Redir',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VirtualHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('extraconf', models.TextField(null=True, blank=True)),
                ('access_log', models.CharField(max_length=200, null=True, blank=True)),
                ('ssl_cert', models.TextField(null=True, blank=True)),
                ('ssl_key', models.TextField(null=True, blank=True)),
                ('ssl_ca', models.TextField(null=True, blank=True)),
                ('clusters', models.ManyToManyField(to='cluster.Cluster')),
            ],
            options={
                'verbose_name_plural': '1- Virtual Host',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VirtualHostType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=200)),
                ('template', models.TextField()),
            ],
            options={
                'verbose_name_plural': '2- Virtual Host Template',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='virtualhost',
            name='virtualhosttype',
            field=models.ForeignKey(verbose_name='Template', to='web.VirtualHostType'),
            preserve_default=True,
        ),
    ]
