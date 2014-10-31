# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('balancer', '0001_initial'),
        ('frontend', '0003_auto_20141030_0820'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='domain',
            options={'verbose_name_plural': '4- Domain'},
        ),
        migrations.AlterModelOptions(
            name='domainalias',
            options={'verbose_name_plural': '3- Domain Alias'},
        ),
        migrations.AlterModelOptions(
            name='virtualhost',
            options={'verbose_name_plural': '1- Virtual Host'},
        ),
        migrations.AlterModelOptions(
            name='virtualhosttype',
            options={'verbose_name_plural': '2- Virtual Host Template'},
        ),
        migrations.AddField(
            model_name='domain',
            name='director',
            field=models.ForeignKey(default=0, to='balancer.Director'),
            preserve_default=False,
        ),
    ]
