# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='domainalias',
            old_name='domain_id',
            new_name='domain',
        ),
    ]
