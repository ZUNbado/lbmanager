# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('balancer', '0005_auto_20150302_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='director',
            name='dirtype_nginx',
            field=models.CharField(default=b'round-robin', max_length=20, verbose_name='Front: Director type', choices=[(b'round-robin', b'Round Robibn'), (b'least_conn', b'Least Connected'), (b'ip_hash', b'Session persistance'), (b'weight', b'Weighted Round Robin')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='director',
            name='dirtype',
            field=models.CharField(default=b'round-robin', max_length=200, verbose_name='Cache: Director type', choices=[(b'Random', ((b'random', b'Random'), (b'client', b'By Client'), (b'hash', b'By Hash'))), (b'round-robin', b'Round Robin'), (b'fallback', b'Fallback')]),
            preserve_default=True,
        ),
    ]
