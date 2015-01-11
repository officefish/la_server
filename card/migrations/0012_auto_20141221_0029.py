# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0011_auto_20141220_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='race',
            field=models.ForeignKey(blank=True, to='card.Race', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='subrace',
            field=models.ForeignKey(blank=True, to='card.SubRace', null=True),
            preserve_default=True,
        ),
    ]
