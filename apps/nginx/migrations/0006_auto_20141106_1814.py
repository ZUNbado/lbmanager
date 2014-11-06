# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx', '0005_location_director'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='director',
            field=models.ManyToManyField(to='balancer.Director', null=True, blank=True),
            preserve_default=True,
        ),
    ]
