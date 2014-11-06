# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='auth_basic_enabled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='ip_allow_enabled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
