# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0013_book'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='heroes',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
    ]
