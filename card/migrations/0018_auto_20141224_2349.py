# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0017_auto_20141224_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardeptitude',
            name='attach_hero',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardeptitude',
            name='attach_initiator',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardeptitude',
            name='attachment',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
