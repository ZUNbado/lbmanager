# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('balancer', '0001_initial'),
        ('nginx', '0004_auto_20141106_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='director',
            field=models.ManyToManyField(to='balancer.Director'),
            preserve_default=True,
        ),
    ]
