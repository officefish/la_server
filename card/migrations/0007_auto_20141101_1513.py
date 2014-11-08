# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0006_auto_20141101_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deck',
            name='items',
            field=models.ManyToManyField(to='card.DeckItem', through='card.DeckCollector'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='deckcollector',
            name='item',
            field=models.ForeignKey(related_name='deck_item', to='card.DeckItem'),
            preserve_default=True,
        ),
    ]
