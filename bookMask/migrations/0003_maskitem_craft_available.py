# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookMask', '0002_auto_20141226_0347'),
    ]

    operations = [
        migrations.AddField(
            model_name='maskitem',
            name='craft_available',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
