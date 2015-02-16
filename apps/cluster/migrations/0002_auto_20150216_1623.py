# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cluster',
            name='persistent',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
