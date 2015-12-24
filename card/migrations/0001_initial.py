# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('book', '__first__'),
        ('hero', '__first__'),
        ('group', '0002_auto_20150413_1809'),
        ('achieve', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(serialize=False,
                                        auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('attack', models.IntegerField(default=1)),
                ('health', models.IntegerField(default=1)),
                ('price', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=200)),
                ('type', models.IntegerField(default=2)),
                ('auxiliary', models.BooleanField(default=False)),
                ('has_weapon', models.BooleanField(default=False)),
                ('widget', models.IntegerField(default=0)),
                ('book', models.ForeignKey(to='book.Book', blank=True, null=True)),
                ('group', models.ForeignKey(to='group.Group', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CardEptitude',
            fields=[
                ('id', models.AutoField(serialize=False,
                                        auto_created=True, primary_key=True, verbose_name='ID')),
                ('period', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('type', models.IntegerField(default=0)),
                ('attachment', models.IntegerField(default=0)),
                ('condition', models.IntegerField(default=0)),
                ('spellCondition', models.IntegerField(default=0)),
                ('attach_hero', models.BooleanField(default=False)),
                ('attach_initiator', models.BooleanField(default=False)),
                ('dynamic', models.BooleanField(default=True)),
                ('battlecry', models.BooleanField(default=False)),
                ('spellSensibility', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=-1)),
                ('lifecycle', models.IntegerField(default=0)),
                ('power', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('max_power', models.IntegerField(default=0)),
                ('probability', models.IntegerField(default=100)),
                ('achieve', models.ForeignKey(
                    to='achieve.Achieve', blank=True, null=True)),
                ('attach_eptitude', models.ForeignKey(to='card.CardEptitude',
                                                      related_name='attach_eptitudes', blank=True, null=True)),
                ('card', models.ForeignKey(to='card.Card', blank=True, null=True)),
                ('dependency', models.ForeignKey(
                    to='card.CardEptitude', blank=True, null=True)),
                ('group', models.ForeignKey(to='group.Group', blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(serialize=False,
                                        auto_created=True, primary_key=True, verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CollectionCollector',
            fields=[
                ('id', models.AutoField(serialize=False,
                                        auto_created=True, primary_key=True, verbose_name='ID')),
                ('collection', models.ForeignKey(to='card.Collection')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CollectionItem',
            fields=[
                ('id', models.AutoField(serialize=False,
                                        auto_created=True, primary_key=True, verbose_name='ID')),
                ('golden', models.BooleanField(default=False)),
                ('count', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=1)),
                ('card', models.ForeignKey(to='card.Card')),
                ('owner', models.ForeignKey(
                    related_name='collectionCards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(serialize=False,
                                        auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('complicated', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeckCollector',
            fields=[
                ('id', models.AutoField(serialize=False,
                                        auto_created=True, primary_key=True, verbose_name='ID')),
                ('deck', models.ForeignKey(to='card.Deck')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeckItem',
            fields=[
                ('id', models.AutoField(serialize=False,
                                        auto_created=True, primary_key=True, verbose_name='ID')),
                ('golden', models.BooleanField(default=False)),
                ('collectionItem', models.ForeignKey(to='card.CollectionItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(serialize=False,
                                        auto_created=True, primary_key=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False,
                                        auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('description', models.CharField(max_length=200)),
                ('race', models.ForeignKey(to='card.Race')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='deckcollector',
            name='item',
            field=models.ForeignKey(related_name='items', to='card.DeckItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deck',
            name='items',
            field=models.ManyToManyField(
                through='card.DeckCollector', to='card.DeckItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deck',
            name='owner',
            field=models.ForeignKey(
                related_name='decks', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deck',
            name='userHero',
            field=models.ForeignKey(
                related_name='decks', blank=True, to='hero.UserHero'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collectioncollector',
            name='item',
            field=models.ForeignKey(
                related_name='collection_item', to='card.CollectionItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collection',
            name='items',
            field=models.ManyToManyField(
                through='card.CollectionCollector', to='card.CollectionItem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collection',
            name='owner',
            field=models.ForeignKey(
                related_name='collections', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardeptitude',
            name='race',
            field=models.ForeignKey(to='card.Race', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardeptitude',
            name='subrace',
            field=models.ForeignKey(to='card.SubRace', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardeptitude',
            name='unit',
            field=models.ForeignKey(
                to='card.Card', related_name='unit', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='race',
            field=models.ForeignKey(to='card.Race', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='subrace',
            field=models.ForeignKey(to='card.SubRace', blank=True, null=True),
            preserve_default=True,
        ),
    ]
