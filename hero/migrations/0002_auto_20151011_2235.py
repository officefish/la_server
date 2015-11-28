# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hero',
            name='health',
            field=models.IntegerField(max_length=2, default=50),
            preserve_default=True,
        ),
    ]
