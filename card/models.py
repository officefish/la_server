from django.db import models

from django.contrib.auth.models import User
from hero.models import UserHero, Hero
from django.contrib import admin
from book.models import Book

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

    def __str__(self):
        return self.title

    @property
    def eptitudes(self):
        return self.cardeptitude_set.all()



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
    card = models.ForeignKey(Card)

    # Момент использования уникальной способности
    # '-1':'ACTIVATED',
    # '0':'START_STEP',
    # '2':'END_STEP',
    # '3':'SELF_PLACED',
    # '4':'ASSOCIATE_PLACED',
    # '5':'OPPONENT_PLACED',
    # '6':'ALL_PLACED',
    # '7':'ASSOCIATE_RACE_PLACED',
    # '8':'OPPONENT_RACE_PLACED',
    # '9':'ALL_RACE_PLACED',
    # '10':'SELF_WOUND',
    # '11':'ASSOCIATE_WOUND',
    # '12':'OPPONENT_WOUND',
    # '13':'ALL_WOUND',
    # '14':'SELF_DIE',
    # '15':'ASSOCIATE_DIE',
    # '16':'OPPONENT_DIE',
    # '17':'ALL_DIE',
    # '18':'ASSOCIATE_TREATED',
    # '19':'OPPONENT_TREATED',
    # '18':'ALL_TREATED',
    # '20':'ASSOCIATE_SPELL',
    # '21':'OPPONENT_SPELL',
    # '22':'ALL_SPELL',
    # '23':'ASSOCIATE_PLAY_CARD',
    # '24':'OPPONENT_PLAY_CARD',
    # '25':'ALL_PLAY_CARD',
    # '26':'ATTACK'
    # '27':'SELF_PLAY'

    period = models.IntegerField(default=0)


    # Уровень использования уникальной способности

    # '0','SELF(к самому себе)',
    # '1','All',
    # '2','RANDOM',
    # '3','SELECTED',
    # '4','LEFT_NEIGHBOR',
    # '5','RIGHT_NEIGHBOR',
    # '6','NEIGHBORS',
    # '7','HERO',
    # '8','DECK',
    # '9','HAND',
    # '10','UNIT_CARDS',
    # '11','SPELL_CARDS',
    # '12','LAST_ATTACKED',
    # '13','LAST_ATTACKED_UNIT',
    # '14','INITIATOR'
    # '15','INITIATOR_UNIT'
    level = models.IntegerField(default=0)

    # Вид уникальной способности
    # DEPENDENCY : 0;
    # JERK : 1; (рывок)
	# DOUBLE_ATTACK:int = 2; (двойная аттака)
	# PASSIVE_ATTACK:int = 3; (пассивная атака)
	# PROVOCATION:int = 4; (провокация)
	# INCREASE_ATTACK:int = 5; (увеличение аттаки)
	# INCREASE_HEALTH:int = 6; (увеличение здоровья)
	# DECREASE_ATTACK:int = 7; (уменьшение аттаки)
	# DECREASE_HEALTH:int = 8; (уменьшение здоровья)
	# CHANGE_ATTACK_TILL:int = 9; (изменение аттаки до)
	# CHANGE_HEALTH_TILL:int = 10; (изменение здоровья до)
	# FULL_HEALTH:int = 11; (полное восстановление здоровья)
	# DUMBNESS:int = 12; (немота)
	# TREATMENT:int = 13; (лечение)
	# PICK_CARD:int = 14; (карта из колоды)
	# BACK_CARD_TO_HAND:int = 15; (возвращение карты в колоду)
	# KILL:int = 16; (убийство)
	# SHADOW:int = 17; (тень)
	# FREEZE:int = 18; (заморозка)
	# NEW_UNIT:int = 19; (новый юнит)
    # SHIELD:int = 20; (божественный щит)
    # INCREASE_ATTACK_MIXIN:int = 21; (доп.увеличение к аттаке)
    # DECREASE_ATTACK_MIXIN:int = 22; (допюцвеличение к здоровью)
    # CAN_NOT_ATTACK:int = 23; (не может аттаковать)
    # REPLACE_ATTACK_HEALTH:int = 24; (меняет местами аттаку и здоровье)
    # SALE:int = 25; (скидка на карту)
    # INCREASE_SPELL:int = 26; (увеличение силы магии)
    # DECREASE_SPELL:int = 27; (умеьшение силы магии)
    # SPELL_INVISIBLE:int = 28; (не доступен для аттак магией)
    # MASSIVE_ATTACK:int = 29; (массовая аттака)
    # INCREASE_ATTACK_AND_HEALTH:int = 30; (увеличение аттаки и здоровья)
    # INCREASE_HEALTH_MIXIN:int = 31; (доп.увеличение к здоровью)
    # DECREASE_HEALTH_MIXIN:int = 32; (доп.уменьщение к здоровью)
    # ENTICE_UNIT:int = 33; (переманивание юнита)
    # NEW_SPELL:int = 34; (новая карта магии)
    # COPY_UNIT:int = 35; (копирование юнита)
    # UNIT_CONVERTION:int = 36; (превращение юнита в другого)

    #  INCREASE_ATTACK_DEPENDS_ON_TOKENS_RACE:int = 38;
    #  INCREASE_HEALTH_DEPENDS_ON_TOKENS_RACE:int = 39;
    #  INCREASE_ATTACK_DEPENDS_ON_TOKENS:int = 40;
    #  INCREASE_HEALTH_DEPENDS_ON_TOKENS:int = 41;
    #  INCREASE_HEALTH_DEPENDS_ON_CARDS:int = 42;
    type = models.IntegerField(default=0)

    # '0':'ASSOCIATE',
    # '1':'OPPONENT',
    # '2':'ALL'
    attachment = models.IntegerField(default=0)

    # '0':'NO_CONDITION'
    # '1':'HAS_WEAPON'
    condition = models.IntegerField(default=0)


    attach_hero = models.BooleanField (default=False)
    attach_initiator = models.BooleanField (default = False)
    dynamic = models.BooleanField (default=True)

    unit = models.ForeignKey(Card, blank=True, null=True, related_name='unit')
    race = models.ForeignKey(Race, blank= True, null=True)
    subrace = models.ForeignKey (SubRace, blank=True, null=True)

    lifecycle =  models.IntegerField(default=0)

    power = models.IntegerField(default=0)
    dependency = models.ForeignKey('self',blank= True, null=True)






