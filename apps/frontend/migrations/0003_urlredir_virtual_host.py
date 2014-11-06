# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx', '0007_nginxvirtualhost_redirect_type'),
        ('frontend', '0002_domain_virtual_host'),
    ]

    operations = [
        migrations.AddField(
            model_name='urlredir',
            name='virtual_host',
            field=models.ForeignKey(default=1, to='nginx.NginxVirtualHost'),
            preserve_default=False,
        ),
    ]
