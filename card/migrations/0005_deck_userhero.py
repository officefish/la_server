# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0001_initial'),
        ('card', '0004_auto_20141031_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='userHero',
            field=models.ForeignKey(related_name='user_hero', default='', blank=True, to='hero.UserHero'),
            preserve_default=False,
        ),
    ]
