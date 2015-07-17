# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achieve', '0003_userachieveitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievemask',
            name='max_access',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
