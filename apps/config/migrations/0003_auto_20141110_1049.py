# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_auto_20141109_1725'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='nginx_sites_dir',
            new_name='nginx_dir',
        ),
    ]
