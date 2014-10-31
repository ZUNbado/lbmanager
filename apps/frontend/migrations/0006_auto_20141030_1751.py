# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0005_auto_20141030_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostRedir',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('enabled', models.BooleanField(default=True)),
                ('domain', models.ForeignKey(to='frontend.Domain')),
            ],
            options={
                'verbose_name_plural': '5- Host Redir',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='domain',
            options={'verbose_name_plural': '3- Domain'},
        ),
        migrations.AlterModelOptions(
            name='domainalias',
            options={'verbose_name_plural': '4- Domain Alias'},
        ),
        migrations.AlterField(
            model_name='virtualhost',
            name='access_log',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='virtualhost',
            name='extraconf',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='virtualhost',
            name='http_ports',
            field=models.IntegerField(default=80, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='virtualhost',
            name='https_ports',
            field=models.IntegerField(default=443, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='virtualhost',
            name='ssl_ca',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='virtualhost',
            name='ssl_cert',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='virtualhost',
            name='ssl_key',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
