#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'inozemcev'


from django.template.response import TemplateResponse, HttpResponse
from django.contrib.auth.models import User

import logging
import json
logger =  logging.getLogger('game_handler')

from hero.models import UserHero, Hero
from card.models import Deck, DeckCollector, DeckItem

from card.models import Card

from userprofile.models import UserProfile

def selectDeck (request):
    id = request.GET['user_id']
    deckId = request.GET['deck_id']
    heroId = request.GET['hero_id']

    user = User.objects.get(id=id)
    profile = UserProfile.objects.get(user=user)

    deck = Deck.objects.get(id=deckId)
    userHero = UserHero.objects.get(id=heroId)

    profile.actual_deck = deck
    profile.actual_hero = userHero
    profile.save()

    response_data = {}
    response_data['deck_id'] =  profile.actual_deck.id
    response_data['hero_id'] =  profile.actual_hero.id
    response_data['hero_uid'] = profile.actual_hero.hero.uid
    response_data['level'] = profile.actual_hero.level

    return HttpResponse(json.dumps(response_data), content_type="application/json")





def getDeckList (request):
    id = request.GET['user_id']

    success = False
    response_data = {}

    '''
    if int(id) == request.user.id:
         success = True
         response_data['status'] = 'success'
    else:
         response_data['status'] = 'error'
         response_data['text'] = 'The request user id and authontificated user id is not the same. (auth.id:%s)' % request.user.id
    '''

    success = True

    if (success):
        user = User.objects.get(id=id)
        heroes = UserHero.objects.filter(owner=user)

        if len(heroes) == 0:
            hero = Hero.objects.get(vocation='adventurer')
            _userHero = UserHero.objects.create(owner=user, hero=hero)
            response_data['hero'] = _userHero.hero.title
            heroes = [_userHero]

        responseHeroes = []
        for userHero in heroes:
              _userHero = userHero
              heroData = {}
              heroData['title'] = userHero.hero.title
              heroData['vocation'] = userHero.hero.vocation
              heroData['description'] = userHero.hero.description
              heroData['uid'] = userHero.hero.uid
              heroData['id'] = userHero.id
              heroData['level'] = userHero.level
              if userHero.decks.count() == 0:
                   create_default_decks(userHero)

              decks = []
              for deck in userHero.decks.all() :
                  deckData = {}
                  deckData['title'] = deck.title
                  deckData['complicated'] = deck.complicated
                  deckData['cardsCount'] = deck.items.count()
                  deckData['id'] = deck.id
                  decks.append(deckData)

              heroData['decks'] = decks

              responseHeroes.append(heroData)

        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)

        actual_deck = profile.actual_deck
        if actual_deck == None:
            actual_deck = Deck.objects.filter(complicated=True, userHero=_userHero)[0]

        actual_hero = profile.actual_hero
        if actual_hero == None:
            actual_hero = _userHero

        response_data['heroes'] = responseHeroes
        response_data['heroesCount'] = len(heroes)
        response_data['status'] = 'success'
        response_data['actual_hero'] = actual_hero.id
        response_data['actual_deck'] = actual_deck.id

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def create_default_decks (userHero):
    deck = Deck.objects.create(userHero=userHero, complicated=True, title='adventurer1')

    #1 Щитоносец (id:18)
    card = Card.objects.get(id=18)

    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)
    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)

    #2 Содлат златоземья (id:16)
    card = Card.objects.get(id=16)

    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)
    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)

    #3 Знахарь вуду (id:8)
    card = Card.objects.get(id=8)

    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)
    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)

    #4 Ящер кровавой топи (id:42)
    card = Card.objects.get(id=42)

    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)
    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)

    #5 Инженер новичек (id:29)
    card = Card.objects.get(id=29)

    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)
    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)

    #6 Амарийский берсек (id:20)
    card = Card.objects.get(id=20)

    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)
    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)

    #7 Охотница на иглошкурых (id:58)
    card = Card.objects.get(id=58)

    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)
    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)

    #8 Лидер рейда (id:52)
    card = Card.objects.get(id=52)

    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)
    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)

    #9 Гризли сталемех (id:50)
    card = Card.objects.get(id=50)

    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)
    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)

    #10 Щитоносец Сен'джин (id:91)
    card = Card.objects.get(id=91)

    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)
    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)

    #11 Ночной клинок (id:102)
    card = Card.objects.get(id=102)

    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)
    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)

    #12 Нага целительница (id:100)
    card = Card.objects.get (id=100)

    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)
    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)

    #13 Рыцарь длани (id:105)
    card = Card.objects.get (id=105)

    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)
    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)

    #14 Гоблин телохранитель (id:97)
    card = Card.objects.get (id=97)

    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)
    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)

    #15 Повелитель арены (id:113)
    card = Card.objects.get (id=113)

    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)
    item = DeckItem.objects.create(card=card, golden=False)
    DeckCollector.objects.create(item=item, deck=deck)

    Deck.objects.create(userHero=userHero, complicated=False, title='adventurer2')
    Deck.objects.create(userHero=userHero, complicated=False, title='adventurer3')











