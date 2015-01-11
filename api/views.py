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
from card.models import Collection, CollectionItem, CollectionCollector

from card.models import Card

from userprofile.models import UserProfile

from bookMask.models import BookMask

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
            UserHero.objects.create(owner=user, hero=hero)

        try:
            Collection.objects.get (owner=user)
        except Collection.DoesNotExist:
            collection = Collection.objects.create (owner=user)
            generateDefaultCollection (user, collection)

        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)

        if user.decks.count() == 0:
            userHero = heroes[0]
            create_default_deck(user, userHero)

        actual_deck = profile.actual_deck

        if actual_deck == None:
            profile.actual_deck = user.decks.all()[0]
            profile.save()
            actual_deck = profile.actual_deck

        initDecks (user, response_data)
        response_data['status'] = 'success'
        response_data['actual_deck'] = actual_deck.id
        response_data['hero'] = None

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def getHeroes (request):
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
            UserHero.objects.create(owner=user, hero=hero)


        responseHeroes = []
        for userHero in heroes:
              heroData = {}
              heroData['title'] = userHero.hero.title
              heroData['vocation'] = userHero.hero.vocation
              heroData['description'] = userHero.hero.description
              heroData['uid'] = userHero.hero.uid
              heroData['id'] = userHero.id
              heroData['level'] = userHero.level
              responseHeroes.append(heroData)

        response_data['heroes'] = responseHeroes
        response_data['status'] = 'success'

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def editDeck (request):
    id = request.GET['user_id']
    deckId = request.GET['deck_id']

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
        deck = Deck.objects.get(id = deckId)
        deckData = {}
        deckData['title'] = deck.title
        deckData['complicated'] = deck.complicated
        deckData['cardsCount'] = deck.items.count()
        deckData['id'] = deck.id
        deckData['uid'] = deck.userHero.hero.uid

        items = []
        for item in deck.items.all():
            collectionItem = item.collectionItem
            itemData = {}
            itemData['count'] = collectionItem.count
            itemData['golden'] = collectionItem.golden
            itemData['id'] = collectionItem.id
            itemData['price'] = collectionItem.card.price
            itemData['title'] = collectionItem.card.title
            itemData['description'] = collectionItem.card.description
            itemData['attack'] = collectionItem.card.attack
            itemData['health'] = collectionItem.card.health
            itemData['type'] = collectionItem.card.type
            if collectionItem.card.race:
                itemData['race'] = collectionItem.card.race.title
            if collectionItem.card.subrace:
                itemData['subrace'] = collectionItem.card.subrace.title
            items.append (itemData)
        deckData['items'] = items

        response_data['deck'] = deckData

        userHero = deck.userHero
        initBooks(user, userHero, response_data)
        initHero (userHero, response_data)

        response_data['status'] = 'success'
        return HttpResponse(json.dumps(response_data), content_type="application/json")








def removeDeck (request):
    id = request.GET['user_id']
    deckId = request.GET['deck_id']

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
        deck = Deck.objects.get(id = deckId)
        deck.delete()

        initCollection (user, response_data)
        initDecks (user, response_data)

        response_data['status'] = 'success'

        return HttpResponse(json.dumps(response_data), content_type="application/json")





def saveDeck (request):
    id = request.GET['user_id']
    request_data = request.GET['data']
    request_data = json.loads (request_data)

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

        deckId = request_data['deckId']
        items = request_data['items']
        deckTitle = request_data['deckTitle']

        deck = Deck.objects.get(id = deckId)

        for item in deck.items.all():
            item.delete()

        for itemData in items:

            itemId = itemData['id']
            collectionItem = CollectionItem.objects.get(id = itemId)
            count = itemData['count']
            golden = itemData['golden']
            for i in range(count):
                deckItem = DeckItem.objects.create(collectionItem=collectionItem, golden=golden)
                DeckCollector.objects.create(item=deckItem, deck=deck)

        deck.title = deckTitle
        if deck.items.count() < 30:
            deck.complicated = False
        else:
            deck.complicated = True
        deck.save()

        # защита от хакеров (нельзя сохранять больше 30 карт)
        if deck.items.count() > 30:
            for item in deck.items.all():
                item.delete()
            deck.complicated = False
            deck.save()

        initCollection (user, response_data)
        initDecks (user, response_data)

        response_data['status'] = 'success'


        return HttpResponse(json.dumps(response_data), content_type="application/json")


def initDecks (user, response_data):
    decks = []
    userDecks = Deck.objects.filter(owner=user)
    for deck in userDecks:
        deckData = {}
        deckData['title'] = deck.title
        deckData['complicated'] = deck.complicated
        deckData['cardsCount'] = deck.items.count()
        deckData['id'] = deck.id
        deckData['uid'] = deck.userHero.hero.uid
        deckData['userHero'] = initHero(deck.userHero, response_data)
        decks.append(deckData)

    response_data['decks'] = decks

def initHero (userHero, response_data):
    heroData = {}
    heroData['title'] = userHero.hero.title
    heroData['vocation'] = userHero.hero.vocation
    heroData['description'] = userHero.hero.description
    heroData['uid'] = userHero.hero.uid
    heroData['id'] = userHero.id
    heroData['level'] = userHero.level
    response_data['hero'] = heroData

    return heroData

def initBooks (user, userHero, response_data):
    collection =  Collection.objects.get (owner=user)
    response_data['books'] = []

    books = {}


    hero = userHero.hero
    heroBooks = hero.book_set.all()

    items = collection.items.all()
    for item in items:
        itemData = {}
        itemData['count'] = item.count
        itemData['golden'] = item.golden
        itemData['id'] = item.id
        itemData['price'] = item.card.price
        itemData['title'] = item.card.title
        itemData['description'] = item.card.description
        itemData['attack'] = item.card.attack
        itemData['health'] = item.card.health
        itemData['type'] = item.card.type
        if item.card.race:
            itemData['race'] = item.card.race.title
        if item.card.subrace:
            itemData['subrace'] = item.card.subrace.title
        book_id = str(item.card.book.id)
        if hasAttr(books, book_id) == False:
            books[book_id] = {}
            books[book_id]['title'] = item.card.book.title
            books[book_id]['description'] = item.card.book.description
            books[book_id]['id'] = item.card.book.id
            books[book_id]['cards'] = []

        books[book_id]['cards'].append (itemData)

    for book in books:
        if heroCollectionContainsBook (books[book], heroBooks):
            response_data['books'].append (books[book])

    response_data['count'] = collection.items.count()

def initCollection (user, response_data):
    collection = Collection.objects.get (owner=user)
    response_data['books'] = []

    books = {}

    items = collection.items.all()
    response_data['count'] = collection.items.count()


    for item in items:
        itemData = {}
        itemData['count'] = item.count
        itemData['golden'] = item.golden
        itemData['id'] = item.id
        itemData['price'] = item.card.price
        itemData['title'] = item.card.title
        itemData['description'] = item.card.description
        itemData['attack'] = item.card.attack
        itemData['health'] = item.card.health
        itemData['type'] = item.card.type
        if item.card.race:
            itemData['race'] = item.card.race.title
        if item.card.subrace:
            itemData['subrace'] = item.card.subrace.title
        book_id = str(item.card.book.id)
        if hasAttr(books, book_id) == False:
            books[book_id] = {}
            books[book_id]['title'] = item.card.book.title
            books[book_id]['description'] = item.card.book.description
            books[book_id]['cards'] = []

        books[book_id]['cards'].append (itemData)

    for book in books:
        response_data['books'].append (books[book])



def createDeck (request):
    id = request.GET['user_id']
    hero_id = request.GET['hero_id']

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
        userHero = UserHero.objects.get(id=hero_id)

        initBooks(user, userHero, response_data)
        initHero (userHero, response_data)

        heroesCount = 0
        deck = Deck.objects.create (userHero=userHero, complicated=False, owner=user)
        for deck in userHero.decks.all():
            if deck.userHero.hero.vocation == userHero.hero.vocation:
                heroesCount = heroesCount + 1

        if heroesCount > 1:
            deck.title = userHero.hero.vocation + str(heroesCount)
        else:
            deck.title = userHero.hero.vocation
        deck.save()

        deckData = {}
        deckData['title'] =  deck.title
        deckData['id'] = deck.id
        deckData['complicated'] = deck.complicated
        deckData['cardsCount'] = deck.items.count()
        response_data['deck'] = deckData

        response_data['status'] = 'success'
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def heroCollectionContainsBook (bookData, heroBooks):
    response = False
    for book in heroBooks:
        if book.id == bookData['id']:
            response = True

    return response


def getCollection (request):
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
        try:
            collection = Collection.objects.get (owner=user)
        except Collection.DoesNotExist:
            collection = Collection.objects.create (owner=user)
            generateDefaultCollection (user, collection)

        response_data['books'] = []

        books = {}

        items = collection.items.all()
        response_data['count'] = collection.items.count()


        for item in items:
            itemData = {}
            itemData['count'] = item.count
            itemData['golden'] = item.golden
            itemData['id'] = item.id
            itemData['price'] = item.card.price
            itemData['title'] = item.card.title
            itemData['description'] = item.card.description
            itemData['attack'] = item.card.attack
            itemData['health'] = item.card.health
            itemData['type'] = item.card.type
            if item.card.race:
                itemData['race'] = item.card.race.title
            if item.card.subrace:
                itemData['subrace'] = item.card.subrace.title
            book_id = str(item.card.book.id)
            if hasAttr(books, book_id) == False:
                books[book_id] = {}
                books[book_id]['title'] = item.card.book.title
                books[book_id]['description'] = item.card.book.description
                books[book_id]['cards'] = []

            books[book_id]['cards'].append (itemData)

        for book in books:
            response_data['books'].append (books[book])


        initDecks (user, response_data)
        response_data['status'] = 'success'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

def hasAttr (obj, attr):
    try:
        obj[attr]
        return True
    except AttributeError:
        return False
    except KeyError:
        return False

def generateDefaultCollection (user, collection):
    userHeroes = UserHero.objects.filter(owner=user)

    for userHero in userHeroes:
        hero = userHero.hero
        books = hero.book_set.all()

        for book in books:
            try:
                mask = BookMask.objects.get(book=book)
                generateByMask (mask, collection)
            except BookMask.DoesNotExist:
                pass

def generateByMask (mask, collection):
     for item in mask.items.all():
          if item.access_simple:
              collectionItem = CollectionItem.objects.create(
                 card = item.card,
                 owner = collection.owner,
                 count = item.access_simple,
                 golden = False,
                 level = 1
              )
              CollectionCollector.objects.create(collection=collection, item=collectionItem)
          if item.access_golden:
              collectionItem = CollectionItem.objects.create(
                 card = item.card,
                 owner = collection.owner,
                 count = item.access_golden,
                 golden = True,
                 level = 1
              )
              CollectionCollector.objects.create(collection=collection, item=collectionItem)



def create_deck_item (user, card, deck, count):
    collectionItem = CollectionItem.objects.get (card=card, owner=user)
    for i in range(count):
        deckItem = DeckItem.objects.create(collectionItem=collectionItem, golden=False)
        DeckCollector.objects.create(item=deckItem, deck=deck)


def create_default_deck (user, userHero):
    deck = Deck.objects.create(owner=user, userHero=userHero, complicated=False, title='adventurer')

    #1 Дракономеханик (id:77)
    card = Card.objects.get(id=77)
    create_deck_item(user, card, deck, 2)

    #2 Содлат златоземья (id:16)
    card = Card.objects.get(id=16)
    create_deck_item(user, card, deck, 2)

    #3 Знахарь вуду (id:8)
    card = Card.objects.get(id=8)
    create_deck_item(user, card, deck, 2)

    #4 Ящер кровавой топи (id:42)
    card = Card.objects.get(id=42)
    create_deck_item(user, card, deck, 2)

    #5 Инженер новичек (id:29)
    card = Card.objects.get(id=29)
    create_deck_item(user, card, deck, 2)

    #6 Дворф диверсант (id:98)
    card = Card.objects.get(id=98)
    create_deck_item(user, card, deck, 2)

    #7 Охотница на иглошкурых (id:58)
    card = Card.objects.get(id=58)
    create_deck_item(user, card, deck, 2)

    #8 Лидер рейда (id:52)
    card = Card.objects.get(id=52)
    create_deck_item(user, card, deck, 2)

    #9 Гризли сталемех (id:50)
    card = Card.objects.get(id=50)
    create_deck_item(user, card, deck, 2)

    #10 Щитоносец Сен'джин (id:91)
    card = Card.objects.get(id=91)
    create_deck_item(user, card, deck, 2)

    #11 Ночной клинок (id:102)
    card = Card.objects.get(id=102)
    create_deck_item(user, card, deck, 2)

    #12 Нага целительница (id:100)
    card = Card.objects.get (id=100)
    create_deck_item(user, card, deck, 2)

    #13 Берсек Гурубаши (id:94)
    card = Card.objects.get (id=94)
    create_deck_item(user, card, deck, 2)

    #14 Гоблин телохранитель (id:97)
    card = Card.objects.get (id=97)
    create_deck_item(user, card, deck, 2)

    #15 Повелитель арены (id:113)
    card = Card.objects.get (id=113)
    create_deck_item(user, card, deck, 2)

    if deck.items.count() == 30:
        deck.complicated = True
        deck.save()

    return deck













