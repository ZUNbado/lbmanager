# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0008_group_last_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='version',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
