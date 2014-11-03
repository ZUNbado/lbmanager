# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('temp_dir', models.CharField(default=b'/tmp/lbmanager', max_length=200)),
                ('nginx_maps_dir', models.CharField(max_length=200)),
                ('nginx_conf_dir', models.CharField(max_length=200)),
                ('nginx_sites_dir', models.CharField(max_length=200)),
                ('ldirectord_conf', models.CharField(max_length=200)),
                ('varnish_dir', models.CharField(max_length=200)),
                ('enable_transfer', models.BooleanField(default=True)),
                ('enable_reload', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('address', models.IPAddressField()),
                ('ssh_user', models.CharField(max_length=200)),
                ('ssh_password', models.CharField(max_length=200)),
                ('ssh_port', models.IntegerField(default=22)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='config',
            name='group',
            field=models.OneToOneField(to='config.Group'),
            preserve_default=True,
        ),
    ]
