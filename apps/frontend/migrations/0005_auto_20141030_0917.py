# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0004_auto_20141030_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='virtualhost',
            name='access_log',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='virtualhost',
            name='extraconf',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='virtualhost',
            name='http_ports',
            field=models.IntegerField(default=80, null=True),
        ),
        migrations.AlterField(
            model_name='virtualhost',
            name='https_ports',
            field=models.IntegerField(default=443, null=True),
        ),
        migrations.AlterField(
            model_name='virtualhost',
            name='ssl_ca',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='virtualhost',
            name='ssl_cert',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='virtualhost',
            name='ssl_key',
            field=models.TextField(null=True),
        ),
    ]
