# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('card', '0025_deck_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectionitem',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1, related_name='collectionCards'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='collection',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='collections'),
            preserve_default=True,
        ),
    ]
