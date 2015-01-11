# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '__first__'),
        ('card', '0021_auto_20141225_0152'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookMask',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('book', models.OneToOneField(to='book.Book')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MaskCollector',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MaskItem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('rarity', models.IntegerField(default=0)),
                ('buy_cost', models.IntegerField(default=0)),
                ('sale_cost', models.IntegerField(default=0)),
                ('access_simple', models.IntegerField(default=0)),
                ('max_simple', models.IntegerField(default=0)),
                ('access_golden', models.IntegerField(default=0)),
                ('max_golden', models.IntegerField(default=0)),
                ('card', models.OneToOneField(to='card.Card')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='maskcollector',
            name='item',
            field=models.ForeignKey(to='bookMask.MaskItem', related_name='mask_item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='maskcollector',
            name='mask',
            field=models.ForeignKey(to='bookMask.BookMask'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bookmask',
            name='items',
            field=models.ManyToManyField(through='bookMask.MaskCollector', to='bookMask.MaskItem'),
            preserve_default=True,
        ),
    ]
