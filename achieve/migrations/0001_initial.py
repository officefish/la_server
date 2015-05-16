# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achieve',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=70)),
                ('description', models.CharField(max_length=200)),
                ('price', models.IntegerField(default=0)),
                ('autonomic', models.BooleanField(default=False)),
                ('type', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AchieveCollector',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('achieve', models.ForeignKey(to='achieve.Achieve')),
                ('owner', models.ForeignKey(related_name='achieve_owner', to='hero.Hero')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AchieveMask',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('rarity', models.IntegerField(default=0)),
                ('buy_cost', models.IntegerField(default=40)),
                ('sale_cost', models.IntegerField(default=10)),
                ('achieve', models.ForeignKey(to='achieve.Achieve')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='achieve',
            name='owners',
            field=models.ManyToManyField(to='hero.Hero', through='achieve.AchieveCollector'),
            preserve_default=True,
        ),
    ]
