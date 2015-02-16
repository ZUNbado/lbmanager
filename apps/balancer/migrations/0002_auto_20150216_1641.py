# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('balancer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='backend',
            name='host_header',
        ),
        migrations.AlterField(
            model_name='director',
            name='dirtype',
            field=models.CharField(default=b'round-robin', max_length=200, verbose_name='Director type', choices=[(b'Random', ((b'random', b'Random'), (b'client', b'By Client'), (b'hash', b'By Hash'))), (b'round-robin', b'Round Robin'), (b'fallback', b'Fallback')]),
            preserve_default=True,
        ),
    ]
