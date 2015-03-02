# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def copybackenddirectors(apps, schema_editor):
    Director = apps.get_model('balancer', 'Director')
    DirectorBackendWeight = apps.get_model('balancer', 'DirectorBackendWeight')

    for d in Director.objects.all():
        for b in d.backends.all():
            DirectorBackendWeight.objects.get_or_create(director=d, backend=b)

class Migration(migrations.Migration):

    dependencies = [
        ('balancer', '0003_auto_20150226_1026'),
    ]

    operations = [
        migrations.CreateModel(
            name='DirectorBackendWeight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('weight', models.IntegerField(null=True, blank=True)),
                ('backend', models.ForeignKey(to='balancer.Backend')),
                ('director', models.ForeignKey(to='balancer.Director')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(copybackenddirectors),
        migrations.RemoveField(
            model_name='director',
            name='backends',
        ),
        migrations.AddField(
            model_name='director',
            name='backends_weight',
            field=models.ManyToManyField(related_name='BackendWeight', through='balancer.DirectorBackendWeight', to='balancer.Backend'),
            preserve_default=True,
        ),
    ]
