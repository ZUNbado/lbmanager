# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx', '0002_authuser_encrypted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nginxvirtualhost',
            name='location',
        ),
        migrations.AddField(
            model_name='location',
            name='nginx_virtualhost',
            field=models.ForeignKey(default=0, to='nginx.NginxVirtualHost'),
            preserve_default=False,
        ),
    ]
