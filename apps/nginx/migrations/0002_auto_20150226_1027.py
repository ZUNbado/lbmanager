# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='location',
            unique_together=set([('path_url', 'nginx_virtualhost')]),
        ),
    ]
