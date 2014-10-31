# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('balancer', '0002_remove_backend_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='backend',
            name='enabled',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='director',
            name='enabled',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
