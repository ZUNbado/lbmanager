# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_auto_20141029_1815'),
    ]

    operations = [
        migrations.CreateModel(
            name='VirtualHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('http_ports', models.IntegerField(default=80)),
                ('https_ports', models.IntegerField(default=443)),
                ('extraconf', models.TextField()),
                ('access_log', models.CharField(max_length=200)),
                ('ssl_cert', models.TextField()),
                ('ssl_key', models.TextField()),
                ('ssl_ca', models.TextField()),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VirtualHostType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('template', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='virtualhost',
            name='virtualhosttype',
            field=models.ForeignKey(to='frontend.VirtualHostType'),
            preserve_default=True,
        ),
    ]
