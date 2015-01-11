# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0020_auto_20141225_0140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardeptitude',
            name='has_weapon',
        ),
        migrations.AddField(
            model_name='card',
            name='has_weapon',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
