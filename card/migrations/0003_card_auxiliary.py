# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0002_card_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='auxiliary',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
