# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('balancer', '0002_remove_director_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='backend',
            options={'verbose_name': 'Backend'},
        ),
        migrations.AlterModelOptions(
            name='director',
            options={'verbose_name': 'Director'},
        ),
    ]
