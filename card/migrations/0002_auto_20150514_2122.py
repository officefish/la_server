# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('achieve', '0002_auto_20150513_1902'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('card', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AchieveCollection',
            fields=[
                ('id', models.AutoField(primary_key=True,
                                        verbose_name='ID', auto_created=True, serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AchieveCollectionItem',
            fields=[
                ('id', models.AutoField(primary_key=True,
                                        verbose_name='ID', auto_created=True, serialize=False)),
                ('achieve', models.ForeignKey(to='achieve.Achieve')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                            related_name='collectionAchieves')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AchieveCollector',
            fields=[
                ('id', models.AutoField(primary_key=True,
                                        verbose_name='ID', auto_created=True, serialize=False)),
                ('collection', models.ForeignKey(to='card.AchieveCollection')),
                ('item', models.ForeignKey(to='card.AchieveCollectionItem',
                                           related_name='achieve_collection_item')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='achievecollection',
            name='items',
            field=models.ManyToManyField(
                to='card.AchieveCollectionItem', through='card.AchieveCollector'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='achievecollection',
            name='owner',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL, related_name='achieve_collections'),
            preserve_default=True,
        ),
    ]
