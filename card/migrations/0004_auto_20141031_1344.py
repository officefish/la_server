# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('card', '0003_card_auxiliary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CollectionCollector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collection', models.ForeignKey(to='card.Collection')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CollectionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('golden', models.BooleanField(default=False)),
                ('count', models.IntegerField(default=0)),
                ('card', models.ForeignKey(to='card.Card')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeckCollector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deck', models.ForeignKey(to='card.Deck')),
                ('item', models.ForeignKey(related_name='deck_item', to='card.CollectionItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeckItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('golden', models.BooleanField(default=False)),
                ('card', models.ForeignKey(to='card.Card')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='deck',
            name='items',
            field=models.ManyToManyField(to='card.CollectionItem', through='card.DeckCollector'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collectioncollector',
            name='item',
            field=models.ForeignKey(related_name='collection_item', to='card.CollectionItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collection',
            name='items',
            field=models.ManyToManyField(to='card.CollectionItem', through='card.CollectionCollector'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collection',
            name='owner',
            field=models.ForeignKey(related_name='collection_owner', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
