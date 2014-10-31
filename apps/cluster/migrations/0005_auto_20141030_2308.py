# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0004_auto_20141030_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='address',
            field=models.IPAddressField(),
            preserve_default=True,
        ),
    ]
