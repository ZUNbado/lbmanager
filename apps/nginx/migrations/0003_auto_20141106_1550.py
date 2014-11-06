# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nginx', '0002_auto_20141106_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='auth_basic_msg',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='ip_allow_list',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='location',
            name='users',
            field=models.ManyToManyField(to='nginx.AuthUser', null=True, blank=True),
            preserve_default=True,
        ),
    ]
