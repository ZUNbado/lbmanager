# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx', '0004_auto_20141106_1626'),
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='virtual_host',
            field=models.ForeignKey(default=1, to='nginx.NginxVirtualHost'),
            preserve_default=False,
        ),
    ]
