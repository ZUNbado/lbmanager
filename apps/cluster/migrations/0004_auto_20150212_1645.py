# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0003_remove_cluster_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cluster',
            options={'verbose_name': 'Service IP Cluster'},
        ),
        migrations.AlterModelOptions(
            name='member',
            options={'verbose_name': 'Member'},
        ),
    ]
