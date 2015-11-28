# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0004_cardeptitude_activate_widget'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardeptitude',
            name='animation',
            field=models.IntegerField(default=-1),
            preserve_default=True,
        ),
    ]
