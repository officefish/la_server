# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0007_auto_20141101_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='title',
            field=models.CharField(default=1, max_length=80),
            preserve_default=False,
        ),
    ]
