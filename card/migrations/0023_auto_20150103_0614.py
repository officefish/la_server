# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0022_collectionitem_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deckitem',
            name='card',
            field=models.ForeignKey(to='card.CollectionItem'),
            preserve_default=True,
        ),
    ]
