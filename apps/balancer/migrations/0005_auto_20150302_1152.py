# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('balancer', '0004_auto_20150302_1141'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='directorbackendweight',
            unique_together=set([('backend', 'director')]),
        ),
    ]
