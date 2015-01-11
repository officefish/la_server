# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0010_auto_20141220_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardeptitude',
            name='race',
            field=models.ForeignKey(to='card.Race', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cardeptitude',
            name='subrace',
            field=models.ForeignKey(to='card.SubRace', null=True, blank=True),
            preserve_default=True,
        ),
    ]
