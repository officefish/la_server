# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weapon', '0001_initial'),
        ('card', '0007_auto_20151014_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardeptitude',
            name='weapon',
            field=models.ForeignKey(to='weapon.Weapon', blank=True, null=True),
            preserve_default=True,
        ),
    ]
