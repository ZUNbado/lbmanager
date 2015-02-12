# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx', '0006_location_access_log'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authuser',
            options={'verbose_name': 'Web Auth User', 'verbose_name_plural': 'Web Auth Users'},
        ),
        migrations.AlterModelOptions(
            name='nginxvirtualhost',
            options={'verbose_name': 'VirtualHost', 'verbose_name_plural': 'VirtualHost'},
        ),
    ]
