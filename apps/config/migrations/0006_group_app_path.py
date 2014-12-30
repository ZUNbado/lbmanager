# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0005_group_admin_port'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='app_path',
            field=models.CharField(default=b'/usr/local/src/lbmanager', max_length=200),
            preserve_default=True,
        ),
    ]
