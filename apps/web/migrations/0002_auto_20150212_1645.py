# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='domain',
            options={'verbose_name': 'Domain'},
        ),
        migrations.AlterModelOptions(
            name='domainalias',
            options={'verbose_name': 'Domain Alias'},
        ),
        migrations.AlterModelOptions(
            name='hostredir',
            options={'verbose_name': 'Host Redir'},
        ),
        migrations.AlterModelOptions(
            name='urlredir',
            options={'verbose_name': 'URL Redir'},
        ),
    ]
