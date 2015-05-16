# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='title',
            field=models.CharField(default='', max_length=70),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.CharField(default='', max_length=200),
            preserve_default=True,
        ),
    ]
