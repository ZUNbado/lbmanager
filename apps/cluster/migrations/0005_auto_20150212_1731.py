# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0004_auto_20150212_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cluster',
            name='protocol',
            field=models.CharField(default=b'tcp', max_length=3, null=True, blank=True, choices=[(b'tcp', b'TCP'), (b'udp', b'UDP')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cluster',
            name='ssl_port',
            field=models.IntegerField(default=443, null=True, blank=True),
            preserve_default=True,
        ),
    ]
