# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0006_auto_20141030_1751'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlRedir',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': '6- URL Redir',
            },
            bases=(models.Model,),
        ),
    ]
