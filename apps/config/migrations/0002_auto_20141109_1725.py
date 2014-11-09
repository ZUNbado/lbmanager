# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name_plural': '1- Group configuration'},
        ),
        migrations.AlterModelOptions(
            name='server',
            options={'verbose_name_plural': '2- Server'},
        ),
    ]
