# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('balancer', '0003_auto_20141030_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backend',
            name='address',
            field=models.IPAddressField(),
            preserve_default=True,
        ),
    ]
