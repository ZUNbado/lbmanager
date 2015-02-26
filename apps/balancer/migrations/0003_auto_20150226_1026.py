# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('balancer', '0002_auto_20150216_1641'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='backend',
            unique_together=set([('server', 'port')]),
        ),
    ]
