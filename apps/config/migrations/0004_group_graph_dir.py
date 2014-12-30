# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0003_auto_20141110_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='graph_dir',
            field=models.CharField(default='/var/lib/collectd/rrd/', max_length=200),
            preserve_default=False,
        ),
    ]
