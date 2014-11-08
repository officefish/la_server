# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0005_deck_userhero'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='complicated',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='deck',
            name='userHero',
            field=models.ForeignKey(related_name='decks', blank=True, to='hero.UserHero'),
            preserve_default=True,
        ),
    ]
