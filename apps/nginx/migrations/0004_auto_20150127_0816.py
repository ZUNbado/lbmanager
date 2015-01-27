# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx', '0003_auto_20141230_1138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authuser',
            options={'verbose_name_plural': '2- Web Auth Users'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={},
        ),
    ]
