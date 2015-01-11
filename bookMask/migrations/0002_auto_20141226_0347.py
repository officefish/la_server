# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookMask', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maskitem',
            name='buy_cost',
            field=models.IntegerField(default=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='maskitem',
            name='max_golden',
            field=models.IntegerField(default=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='maskitem',
            name='max_simple',
            field=models.IntegerField(default=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='maskitem',
            name='sale_cost',
            field=models.IntegerField(default=10),
            preserve_default=True,
        ),
    ]
