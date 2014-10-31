# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0003_auto_20141030_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cluster',
            name='enabled',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='enabled',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
