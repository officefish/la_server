# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hero', '__first__'),
        ('achieve', '0002_auto_20150513_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAchieveItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        primary_key=True, auto_created=True, serialize=False)),
                ('position', models.IntegerField()),
                ('achieve', models.ForeignKey(to='achieve.Achieve')),
                ('owner', models.ForeignKey(
                    related_name='achieves', to='hero.UserHero')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
