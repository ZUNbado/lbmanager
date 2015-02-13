# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigDefaultAdmin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('configdefaultadmin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='config.ConfigDefaultAdmin')),
                ('name', models.CharField(max_length=200)),
                ('temp_dir', models.CharField(max_length=200)),
                ('nginx_dir', models.CharField(max_length=200)),
                ('ldirectord_conf', models.CharField(max_length=200)),
                ('graph_dir', models.CharField(max_length=200)),
                ('varnish_dir', models.CharField(max_length=200)),
                ('admin_port', models.IntegerField(default=8000, null=True, blank=True)),
                ('app_path', models.CharField(default=b'/usr/local/src/lbmanager', max_length=200)),
                ('enable_transfer', models.BooleanField(default=True)),
                ('enable_reload', models.BooleanField(default=True)),
                ('last_update', models.DateTimeField(null=True, blank=True)),
                ('last_apply', models.DateTimeField(null=True, blank=True)),
                ('version', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Group',
            },
            bases=('config.configdefaultadmin',),
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('configdefaultadmin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='config.ConfigDefaultAdmin')),
                ('name', models.CharField(max_length=200)),
                ('address', models.IPAddressField()),
                ('ssh_user', models.CharField(max_length=200, null=True, blank=True)),
                ('ssh_password', models.CharField(max_length=200, null=True, blank=True)),
                ('ssh_port', models.IntegerField(default=22, null=True, blank=True)),
                ('role_cluster', models.BooleanField(default=False)),
                ('role_backend', models.BooleanField(default=False)),
                ('role_frontend', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Server',
            },
            bases=('config.configdefaultadmin',),
        ),
        migrations.AddField(
            model_name='group',
            name='cluster_servers',
            field=models.ManyToManyField(to='config.Server', null=True, blank=True),
            preserve_default=True,
        ),
    ]
