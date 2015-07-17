# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0002_auto_20150514_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievecollectionitem',
            name='count',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
