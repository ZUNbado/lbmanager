# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0002_auto_20141030_2304'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ClusterDefaults',
        ),
        migrations.AddField(
            model_name='cluster',
            name='enabled',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='enabled',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
