# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0004_userhero_level'),
        ('card', '0012_auto_20141221_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=70)),
                ('description', models.CharField(max_length=200)),
                ('heroes', models.ManyToManyField(to='hero.Hero', blank=True, related_name='heroes', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
