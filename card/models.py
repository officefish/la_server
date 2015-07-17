from django.db import models

from django.contrib.auth.models import User
from hero.models import UserHero, Hero
from django.contrib import admin
from book.models import Book
from group.models import Group
from achieve.models import Achieve

class Race (models.Model):
    title = models.CharField (max_length=70)
    description = models.CharField (max_length=200)

class SubRace (models.Model):
    race = models.ForeignKey (Race)
    title = models.CharField (max_length=70)
    description = models.CharField(max_length=200)

# Create your models here.
class Card (models.Model):
    title = models.CharField (max_length=80)
    attack = models.IntegerField(default=1)
    health = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    description = models.CharField (max_length=200)
    type = models.IntegerField (default=2)
    race = models.ForeignKey(Race, blank= True, null=True)
    subrace = models.ForeignKey (SubRace, blank=True, null=True)
    auxiliary = models.BooleanField(default=False)
    book = models.ForeignKey (Book, blank=True, null=True)
    has_weapon = models.BooleanField (default=False)
    widget = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def eptitudes(self):
        return self.cardeptitude_set.all()

    group = models.ForeignKey(Group, blank=True, null=True)

class CardAdmin(admin.ModelAdmin):
    fields = ['title', 'attack', 'health', 'price', 'description', 'type', 'auxiliary']
    list_display = ('title', 'price', 'auxiliary')
    ordering = ['price']

admin.site.register(Card, CardAdmin)

class CollectionItem (models.Model):
    card = models.ForeignKey(Card)
    golden = models.BooleanField(default=False)
    count = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    owner = models.ForeignKey(User, related_name='collectionCards')

    @property
    def price(self):
        return self.card.price

class CollectionItemAdmin (admin.ModelAdmin):
    fields = ['card', 'owner', 'count', 'golden', 'level']

admin.site.register(CollectionItem, CollectionItemAdmin)

class Collection (models.Model):
    owner = models.ForeignKey(User, related_name='collections')
    items = models.ManyToManyField(CollectionItem, through='CollectionCollector')

class CollectionAdmin (admin.ModelAdmin):
    fields = ['owner']
admin.site.register(Collection, CollectionAdmin)

class CollectionCollector (models.Model):
    item = models.ForeignKey(CollectionItem, related_name='collection_item')
    collection = models.ForeignKey(Collection)

class DeckItem (models.Model):
    collectionItem = models.ForeignKey(CollectionItem)
    golden = models.BooleanField(default=False)

class DeckItemAdmin (admin.ModelAdmin):
    fields = ['collectionItem']

admin.site.register(DeckItem, DeckItemAdmin)

class Deck (models.Model):
    title = models.CharField (max_length=80)
    owner = models.ForeignKey(User, related_name='decks')
    userHero = models.ForeignKey(UserHero, related_name='decks',  blank=True)
    items = models.ManyToManyField(DeckItem, through='DeckCollector')
    complicated = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class DeckAdmin (admin.ModelAdmin):
    fields =['title', 'complicated']

admin.site.register(Deck, DeckAdmin)


class DeckCollector (models.Model):
    item = models.ForeignKey(DeckItem, related_name='items')
    deck = models.ForeignKey(Deck)

class CardEptitude (models.Model):
    card = models.ForeignKey(Card, blank=True, null=True)
    achieve = models.ForeignKey(Achieve, blank=True, null=True)

    period = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    type = models.IntegerField(default=0)
    attachment = models.IntegerField(default=0)

    condition = models.IntegerField(default=0)
    spellCondition = models.IntegerField(default=0)

    attach_hero = models.BooleanField (default=False)
    attach_initiator = models.BooleanField (default = False)
    dynamic = models.BooleanField (default=True)

    battlecry = models.BooleanField (default=False)
    spellSensibility = models.BooleanField(default=False)

    unit = models.ForeignKey(Card, blank=True, null=True, related_name='unit')
    race = models.ForeignKey(Race, blank= True, null=True)
    subrace = models.ForeignKey (SubRace, blank=True, null=True)
    group = models.ForeignKey(Group, blank=True, null=True)
    price = models.IntegerField(default=-1)

    lifecycle =  models.IntegerField(default=0)

    power = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    max_power = models.IntegerField(default=0)

    dependency = models.ForeignKey('self',blank= True, null=True)
    attach_eptitude = models.ForeignKey('self', blank=True, null=True, related_name='attach_eptitudes')

    probability = models.IntegerField(default=100)

    activate_widget = models.BooleanField (default=False)

class AchieveCollectionItem (models.Model):
    achieve = models.ForeignKey(Achieve)
    owner = models.ForeignKey(User, related_name='collectionAchieves')
    count = models.IntegerField(default = 1)

    @property
    def price(self):
        return self.achieve.price

class AchieveCollection(models.Model):
    owner = models.ForeignKey(User, related_name='achieve_collections')
    items = models.ManyToManyField(AchieveCollectionItem, through='AchieveCollector')

class AchieveCollector (models.Model):
    item = models.ForeignKey(AchieveCollectionItem, related_name='achieve_collection_item')
    collection = models.ForeignKey(AchieveCollection)












