# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='vocation',
            field=models.CharField(default='', max_length=70, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hero',
            name='description',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
