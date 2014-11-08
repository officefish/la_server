from django.db import models

from django.contrib.auth.models import User
from hero.models import UserHero
from django.contrib import admin



# Create your models here.
class Card (models.Model):
    title = models.CharField (max_length=80)
    attack = models.IntegerField(default=1)
    health = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    description = models.CharField (max_length=200)
    type = models.BooleanField (default=True)
    auxiliary = models.BooleanField(default=False)

    def __str__(self):
        return self.title



class CardAdmin(admin.ModelAdmin):
    fields = ['title', 'attack', 'health', 'price', 'description', 'type', 'auxiliary']
    list_display = ('title', 'price', 'auxiliary')
    ordering = ['price']

admin.site.register(Card, CardAdmin)


class CollectionItem (models.Model):
    card = models.ForeignKey(Card)
    golden = models.BooleanField(default=False)
    count = models.IntegerField(default=0)

class Collection (models.Model):
    owner = models.ForeignKey(User, related_name='collection_owner')
    items = models.ManyToManyField(CollectionItem, through='CollectionCollector')

class CollectionCollector (models.Model):
    item = models.ForeignKey(CollectionItem, related_name='collection_item')
    collection = models.ForeignKey(Collection)

class DeckItem (models.Model):
    card = models.ForeignKey(Card)
    golden = models.BooleanField(default=False)

class Deck (models.Model):
    title = models.CharField (max_length=80)
    userHero = models.ForeignKey(UserHero, related_name='decks',  blank=True)
    items = models.ManyToManyField(DeckItem, through='DeckCollector')
    complicated = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class DeckAdmin (admin.ModelAdmin):
    fields = ['title', 'complicated']

admin.site.register(Deck, DeckAdmin)


class DeckCollector (models.Model):
    item = models.ForeignKey(DeckItem, related_name='deck_item')
    deck = models.ForeignKey(Deck)




