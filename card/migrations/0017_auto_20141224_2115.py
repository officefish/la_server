# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0016_card_dynamic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='dynamic',
        ),
        migrations.AddField(
            model_name='cardeptitude',
            name='dynamic',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
