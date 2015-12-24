from django.db import models

from hero.models import Hero


# Create your models here.
class Book (models.Model):
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=200)
    heroes = models.ManyToManyField(Hero, blank=True, null=True)

    @property
    def cards(self):
        return self.card_set.all().order_by('price')
