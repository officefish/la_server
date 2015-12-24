from django.db import models
from hero.models import Hero, UserHero
from django.db.models.signals import post_save

# Create your models here.


class Achieve (models.Model):
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    autonomic = models.BooleanField(default=False)
    owners = models.ManyToManyField(Hero, through='AchieveCollector')
    type = models.IntegerField(default=0)

    @property
    def eptitudes(self):
        return self.cardeptitude_set.all()


class AchieveCollector (models.Model):
    owner = models.ForeignKey(Hero, related_name='achieve_owner')
    achieve = models.ForeignKey(Achieve)


class AchieveMask (models.Model):
    achieve = models.ForeignKey(Achieve)
    rarity = models.IntegerField(default=0)
    buy_cost = models.IntegerField(default=40)
    sale_cost = models.IntegerField(default=10)
    access = models.IntegerField(default=0)
    max_access = models.IntegerField(default=1)
    craft_available = models.BooleanField(default=True)

    def create_achieve_mask(sender, instance, created, **kwargs):
        if created:
            AchieveMask.objects.create(achieve=instance)

    post_save.connect(create_achieve_mask, sender=Achieve)


class UserAchieveItem (models.Model):
    achieve = models.ForeignKey(Achieve)
    owner = models.ForeignKey(UserHero, related_name='achieves')
    position = models.IntegerField()
