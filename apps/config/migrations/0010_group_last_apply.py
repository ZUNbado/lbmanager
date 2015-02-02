# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0009_group_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='last_apply',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
