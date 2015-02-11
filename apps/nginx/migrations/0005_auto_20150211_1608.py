# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx', '0004_auto_20150127_0816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hostconfig',
            name='group',
        ),
        migrations.DeleteModel(
            name='HostConfig',
        ),
    ]
