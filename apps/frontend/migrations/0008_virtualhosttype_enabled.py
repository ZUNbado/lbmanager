# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0007_urlredir'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualhosttype',
            name='enabled',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
