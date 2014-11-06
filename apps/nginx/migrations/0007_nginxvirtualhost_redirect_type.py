# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx', '0006_auto_20141106_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='nginxvirtualhost',
            name='redirect_type',
            field=models.IntegerField(default=301, choices=[(301, b'Permanent'), (302, b'Temporal')]),
            preserve_default=True,
        ),
    ]
