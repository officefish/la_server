# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0026_auto_20150104_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collectionitem',
            name='owner',
        ),
    ]
