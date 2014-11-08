# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='actual_deck',
            field=models.ForeignKey(blank=True, to='card.Deck', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='actual_hero',
            field=models.ForeignKey(blank=True, to='hero.UserHero', null=True),
            preserve_default=True,
        ),
    ]
