# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0003_achievecollectionitem_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardeptitude',
            name='activate_widget',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
