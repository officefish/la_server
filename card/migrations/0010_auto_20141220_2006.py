# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0009_cardeptitude'),
    ]

    operations = [
        migrations.CreateModel(
            name='EptitudeCondition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=80)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=70)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubRace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=70)),
                ('description', models.CharField(max_length=200)),
                ('race', models.ForeignKey(to='card.Race')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cardeptitude',
            name='condition',
            field=models.ForeignKey(blank=True, null=True, to='card.EptitudeCondition', related_name='condition'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardeptitude',
            name='dependency',
            field=models.ForeignKey(blank=True, null=True, to='card.CardEptitude'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardeptitude',
            name='lifecycle',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
