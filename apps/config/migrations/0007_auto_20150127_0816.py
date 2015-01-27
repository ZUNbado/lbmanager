# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0006_group_app_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='role_backend',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='role_cluster',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='server',
            name='role_frontend',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
