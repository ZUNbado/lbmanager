# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0010_group_last_apply'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Group'},
        ),
        migrations.AlterModelOptions(
            name='server',
            options={'verbose_name': 'Server'},
        ),
    ]
