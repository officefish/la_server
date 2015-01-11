# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0018_auto_20141224_2349'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardeptitude',
            name='has_weapon',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
