# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('card', '0024_auto_20150103_0615'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='decks', default=False),
            preserve_default=False,
        ),
    ]
