# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0003_hero_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='userhero',
            name='level',
            field=models.IntegerField(default=1, max_length=2),
            preserve_default=True,
        ),
    ]
