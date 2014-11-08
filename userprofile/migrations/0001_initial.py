# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0008_deck_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hero', '0004_userhero_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('actual_deck', models.ForeignKey(to='card.Deck', blank=True)),
                ('actual_hero', models.ForeignKey(to='hero.UserHero', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
