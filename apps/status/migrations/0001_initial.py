# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GraphTypes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('conf', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='graph',
            name='graph',
            field=models.ForeignKey(to='status.GraphTypes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='graph',
            name='server',
            field=models.ForeignKey(to='config.Server'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='graph',
            unique_together=set([('graph', 'server')]),
        ),
    ]
