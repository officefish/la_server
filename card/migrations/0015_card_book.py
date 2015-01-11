# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '__first__'),
        ('card', '0014_auto_20141224_0310'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='book',
            field=models.ForeignKey(blank=True, to='book.Book', null=True),
            preserve_default=True,
        ),
    ]
