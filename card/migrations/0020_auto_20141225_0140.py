# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0019_cardeptitude_has_weapon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardeptitude',
            name='condition',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='EptitudeCondition',
        ),
    ]
