from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from hero.models import UserHero
from card.models import Deck


class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    actual_deck = models.ForeignKey(Deck, blank=True, null=True)
    actual_hero = models.ForeignKey(UserHero, blank=True, null=True)

    #
    dust = models.IntegerField(default=15000)
    money = models.IntegerField(default=300)

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)
