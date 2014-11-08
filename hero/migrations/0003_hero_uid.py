# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0002_auto_20141031_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='uid',
            field=models.IntegerField(default=0, max_length=2),
            preserve_default=False,
        ),
    ]
