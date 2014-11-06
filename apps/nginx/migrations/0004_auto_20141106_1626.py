# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx', '0003_auto_20141106_1550'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='path',
            new_name='path_url',
        ),
        migrations.RemoveField(
            model_name='nginxvirtualhost',
            name='template',
        ),
        migrations.DeleteModel(
            name='VirtualHostTemplate',
        ),
        migrations.AddField(
            model_name='location',
            name='backend_type',
            field=models.CharField(default=b'proxy', max_length=5, choices=[(b'proxy', b'Proxy'), (b'files', b'Static')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='path_fs',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nginxvirtualhost',
            name='location',
            field=models.ManyToManyField(to='nginx.Location'),
            preserve_default=True,
        ),
    ]
