# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0001_initial'),
        ('book', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookMask',
            fields=[
                ('id', models.AutoField(serialize=False,
                                        auto_created=True, primary_key=True, verbose_name='ID')),
                ('book', models.OneToOneField(to='book.Book')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MaskCollector',
            fields=[
                ('id', models.AutoField(serialize=False,
                                        auto_created=True, primary_key=True, verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MaskItem',
            fields=[
                ('id', models.AutoField(serialize=False,
                                        auto_created=True, primary_key=True, verbose_name='ID')),
                ('rarity', models.IntegerField(default=0)),
                ('buy_cost', models.IntegerField(default=40)),
                ('sale_cost', models.IntegerField(default=10)),
                ('access_simple', models.IntegerField(default=0)),
                ('max_simple', models.IntegerField(default=2)),
                ('access_golden', models.IntegerField(default=0)),
                ('max_golden', models.IntegerField(default=2)),
                ('craft_available', models.BooleanField(default=True)),
                ('card', models.OneToOneField(to='card.Card')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='maskcollector',
            name='item',
            field=models.ForeignKey(
                related_name='mask_item', to='bookMask.MaskItem'),
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
            field=models.ManyToManyField(
                to='bookMask.MaskItem', through='bookMask.MaskCollector'),
            preserve_default=True,
        ),
    ]
