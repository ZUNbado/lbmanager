# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0004_group_graph_dir'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='admin_port',
            field=models.IntegerField(default=8000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
