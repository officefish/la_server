from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Hero (models.Model):
    title = models.CharField (max_length=70)
    description = models.CharField(max_length=200, blank=True)
    vocation = models.CharField (max_length=70, blank=True)
    uid = models.IntegerField(max_length=2)

    @property
    def short_description (self):
        return str(self.description) [:90] + '...'


class UserHero (models.Model):
    owner = models.ForeignKey(User)
    hero = models.ForeignKey(Hero)
    level = models.IntegerField(max_length=2, default=1)
