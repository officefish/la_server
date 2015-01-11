# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0028_collectionitem_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='type',
            field=models.IntegerField(default=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='deckcollector',
            name='item',
            field=models.ForeignKey(related_name='items', to='card.DeckItem'),
            preserve_default=True,
        ),
    ]
