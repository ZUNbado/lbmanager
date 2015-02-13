# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.core.management import call_command

def loadfixture(apps, schema_editor):
    for fix in [ 'default_group.json', 'groups.json' ]:
        call_command('loaddata', fix)



class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
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
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
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
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='group',
            name='cluster_servers',
            field=models.ManyToManyField(to='config.Server', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RunPython(loadfixture),
    ]
