# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0023_auto_20150103_0614'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deckitem',
            old_name='card',
            new_name='collectionItem',
        ),
    ]
