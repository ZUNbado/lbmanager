# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0002_auto_20150216_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='ssl_port',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
