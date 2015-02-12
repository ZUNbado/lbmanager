# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx', '0007_auto_20150212_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nginxvirtualhost',
            name='redirect_type',
            field=models.IntegerField(default=301, null=True, blank=True, choices=[(301, b'Permanent'), (302, b'Temporal')]),
            preserve_default=True,
        ),
    ]
