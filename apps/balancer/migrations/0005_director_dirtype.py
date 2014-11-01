# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('balancer', '0004_auto_20141030_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='director',
            name='dirtype',
            field=models.CharField(default='hash', max_length=200, choices=[(b'random', b'Random'), (b'client', b'Client'), (b'hash', b'Hash')]),
            preserve_default=False,
        ),
    ]
