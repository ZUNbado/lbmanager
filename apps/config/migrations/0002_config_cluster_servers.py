# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='cluster_servers',
            field=models.ManyToManyField(to='config.Server'),
            preserve_default=True,
        ),
    ]
