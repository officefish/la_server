# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0008_deck_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardEptitude',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('type', models.IntegerField(default=0)),
                ('power', models.IntegerField(default=0)),
                ('card', models.ForeignKey(to='card.Card')),
                ('unit', models.ForeignKey(null=True, blank=True, related_name='unit', to='card.Card')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
