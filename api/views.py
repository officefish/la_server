#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'inozemcev'


from django.template.response import TemplateResponse, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render

import logging
import json
logger =  logging.getLogger('game_handler')

from hero.models import UserHero, Hero
from card.models import Deck, DeckCollector, DeckItem
from card.models import Collection, CollectionItem, CollectionCollector
from card.models import AchieveCollection, AchieveCollectionItem, AchieveCollector
from achieve.models import Achieve, AchieveMask, UserAchieveItem

from card.models import Card

from userprofile.models import UserProfile

from bookMask.models import BookMask, MaskItem
from book.models import Book

def crossdomain(
        request,
        template_name = 'web/crossdomain.xml'):

    return render(request, template_name, content_type='text/xml; charset=utf-8')
    #return HttpResponse(template_name, content_type='text/xml; charset=utf-8' )

def maincrossdomain(
        request,
        template_name = 'crossdomain.xml'):

    return render(request, template_name, content_type='text/xml; charset=utf-8')
    #return HttpResponse(template_name, content_type='text/xml; charset=utf-8' )


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

def destroyAchieve (request):
    id = request.GET['user_id']
    hero_id = request.GET['hero_id']
    achieve_id = request.GET['achieve_id']

    success = True
    response_data = {}

    if success:
         user = User.objects.get(id=id)
         hero = Hero.objects.get(id=hero_id)
         profile = UserProfile.objects.get (user=user)
         achieveFlag = False
         maskFlag = False




         try:
             achieveFlag = True
             achieve = Achieve.objects.get(id=achieve_id)
         except Achieve.DoesNotExist:
             success = False
             error_message = 'AchieveDoesNotExist'
             error_status = 501

         if achieveFlag:
             try:
                 mask = AchieveMask.objects.get(achieve=achieve)
                 maskFlag = True
             except AchieveMask.DoesNotExist:
                 success = False
                 error_message = 'MaskDoesNotExist'
                 error_status = 505

         if maskFlag:
             try:
                 item = AchieveCollectionItem.objects.get(achieve=achieve, owner=user)
                 if item.count == 1:
                     item.delete()
                     response_data['count'] = 0
                 else:
                     item.count = item.count - 1
                     item.save()
                     response_data['count'] = item.count
                 profile.dust += mask.sale_cost
                 profile.save()

             except AchieveCollectionItem.DoesNotExist:
                 success = False
                 error_status = 503
                 error_message = 'NoItemsToDelete'




    if success:
        response_data['status'] =  'success'
        response_data['achieve_id'] = achieve_id
        response_data['dust'] = profile.dust

    else:
        response_data['status'] =  'error'
        response_data['message'] = error_message
        response_data['error_type'] = error_status

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def craftAchieve (request):
    id = request.GET['user_id']
    hero_id = request.GET['hero_id']
    achieve_id = request.GET['achieve_id']

    success = True
    response_data = {}

    if success:
         user = User.objects.get(id=id)
         hero = Hero.objects.get(id=hero_id)
         profile = UserProfile.objects.get (user=user)

         try:
             achieve = Achieve.objects.get(id=achieve_id)
         except Achieve.DoesNotExist:
             success = False
             error_message = 'AchieveDoesNotExist'
             error_status = 501

         try:
            mask = AchieveMask.objects.get(achieve=achieve)
            maskFlag = True
         except AchieveMask.DoesNotExist:
             success = False
             error_message = 'MaskDoesNotExist'
             error_status = 504
             maskFlag = False

         if maskFlag:

             if profile.dust > mask.buy_cost:
                 profile.dust -= mask.buy_cost
                 profile.save()
                 try:
                     item = AchieveCollectionItem.objects.get(achieve=achieve, owner=user)
                     if item.count >= mask.max_access:
                         success = False
                         error_status = 502
                         error_message = 'AchiveWasAlreadyCraftedMaxTimes'
                     else:
                         item.count = item.count + 1
                         item.save()
                 except AchieveCollectionItem.DoesNotExist:
                     item = AchieveCollectionItem.objects.create(achieve=achieve, owner=user, count=1)
                     collection = AchieveCollection.objects.get (owner=user)
                     AchieveCollector.objects.create(item=item, collection=collection)

             else:
                 success = False
                 error_message = 'NotEnoughDust'
                 error_status = 505

    if success:
        response_data['status'] =  'success'
        response_data['achieve_id'] = achieve_id
        response_data['dust'] = profile.dust
        response_data['count'] = item.count
    else:
        response_data['status'] =  'error'
        response_data['message'] = error_message
        response_data['error_type'] = error_status

    return HttpResponse(json.dumps(response_data), content_type="application/json")



def craftAchievesList (request):
    id = request.GET['user_id']
    hero_id = request.GET['hero_id']

    success = True

    response_data = {}

    if success:
         user = User.objects.get(id=id)
         hero = Hero.objects.get(id=hero_id)
         profile = UserProfile.objects.get (user=user)


         achieves = []

         achieveMasks = AchieveMask.objects.filter( craft_available=True, achieve__owners=hero)
         for mask in achieveMasks:
            achieveData = getAchieveData(mask.achieve)
            try:
                item = AchieveCollectionItem.objects.get(achieve=mask.achieve, owner=user)
                achieveData['count'] = item.count
            except AchieveCollectionItem.DoesNotExist:
                achieveData['count'] = 0

                achieveData['max_access'] = mask.max_access
            achieveData['buyCost'] = mask.buy_cost
            achieveData['saleCost'] = mask.sale_cost
            achieveData['max_access'] = mask.max_access
            achieveData['access'] = mask.access


            achieves.append(achieveData)

    response_data['achieves'] = achieves
    response_data['status'] = 'success'
    response_data['dust'] = profile.dust
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def getAchieveData(achieve):
    achieveData = {}
    achieveData['title'] = achieve.title
    achieveData['description'] = achieve.description
    achieveData['price'] = achieve.price
    achieveData['autonomic'] = achieve.autonomic
    achieveData['type'] = achieve.type
    achieveData['id'] = achieve.id
    return achieveData


def setupAchieves (request):
    id = request.GET['user_id']
    hero_id = request.GET['hero_id']
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

    if success:
         user = User.objects.get(id=id)
         hero = Hero.objects.get(id=hero_id)
         userHero = UserHero.objects.get(owner=user, hero=hero)

         for achieve in userHero.achieves.all():
             achieve.delete()

         for i in range(len(request_data['setup'])):
            setupData = request_data['setup'][i]
            achieve = Achieve.objects.get(id=setupData["achieve"])
            UserAchieveItem.objects.create(owner=userHero, achieve=achieve, position=setupData["position"])



    response_data['success'] = success
    return HttpResponse(json.dumps(response_data), content_type="application/json")






def getAchievesList (request):
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
        hero = Hero.objects.get(id=hero_id)
        userHero = UserHero.objects.get(owner=user, hero=hero)

        try:
            collection = AchieveCollection.objects.get (owner=user)
            checkNewAvailableAchieves(user, collection)
        except AchieveCollection.DoesNotExist:
            collection = AchieveCollection.objects.create (owner=user)
            generateDefaultAchieveCollection (user, collection)

        achieves = collection.items.filter(owner=hero)

        achievesData = []
        for achieve in userHero.achieves.all():
            achievesData.append({"achieve":achieve.achieve.id, "position":achieve.position})

    response_data['collection_count'] = collection.items.count()
    response_data['status'] = 'success'
    response_data['achieves'] = getAchievesData(achieves)
    response_data['hero_id'] = hero_id
    response_data['hero_vocation'] = hero.vocation
    response_data['setup'] = achievesData

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def checkNewAvailableAchieves(user, collection):
    achieveMasks = AchieveMask.objects.filter(access=1, craft_available=False)
    for mask in achieveMasks:
        try:
            item = AchieveCollectionItem.objects.get(achieve=mask.achieve, owner=user)
        except AchieveCollectionItem.DoesNotExist:
            item = AchieveCollectionItem.objects.create(achieve=mask.achieve, owner=user, count=1)
            AchieveCollector.objects.create(item=item, collection=collection)

def generateDefaultAchieveCollection (user, collection):
    achieveMasks = AchieveMask.objects.filter(access=1, craft_available=False)
    for mask in achieveMasks:
        item = AchieveCollectionItem.objects.create(achieve=mask.achieve, owner=user, count=1)
        AchieveCollector.objects.create(item=item, collection=collection)


def getAchievesData(achieves):
    data = []

    for item in achieves:
        achieveData = {}
        achieveData['title'] = item.achieve.title
        achieveData['description'] = item.achieve.description
        achieveData['price'] = item.achieve.price
        achieveData['autonomic'] = item.achieve.autonomic
        achieveData['type'] = item.achieve.type
        achieveData['id'] = item.achieve.id
        achieveData['count'] = item.count
        data.append(achieveData)
    return data


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

def updateHeroes (request):
    id = request.GET['user_id']

    user = User.objects.get(id=id)
    heroes = UserHero.objects.filter(owner=user)

    if len(heroes) == 1:
            hero = Hero.objects.get(vocation='shaman')
            UserHero.objects.create(owner=user, hero=hero)

            hero = Hero.objects.get(vocation='rainger')
            UserHero.objects.create(owner=user, hero=hero)

    heroes = UserHero.objects.filter(owner=user)
    response_data = {}
    response_data['totalHeroes'] = len(heroes)
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

    items = collection.items.all().order_by('card__price')
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

def destroyCard (request):
    id = request.GET['user_id']
    user = User.objects.get(id=id)

    cardId = request.GET['card_id']
    card = Card.objects.get (id=cardId)

    golden = request.GET['golden']
    golden = bool(int(golden))

    response_data = {}

    profile = UserProfile.objects.get (user=user)

    maskItem = MaskItem.objects.get (card=card)

    if golden:
        totalCost = maskItem.sale_cost * 2
    else:
        totalCost = maskItem.sale_cost

    try:
        collection = Collection.objects.get (owner=user)
        collectionItem = CollectionItem.objects.get (card=card, owner=collection.owner, golden=golden)

        count = collectionItem.count - 1

        collectionItem.count = count
        collectionItem.save()

        profile.dust = profile.dust + totalCost
        profile.save()

        if count == 0:
            collectionItem.delete()

        response_data['success'] = True
        response_data['count'] = count
        response_data['golden'] = golden
        response_data['dust'] = profile.dust


    except CollectionItem.DoesNotExist:
         response_data['success'] = False

    return HttpResponse(json.dumps(response_data), content_type="application/json")



def craftCard (request):
    id = request.GET['user_id']
    user = User.objects.get(id=id)

    cardId = request.GET['card_id']
    card = Card.objects.get (id=cardId)

    golden = request.GET['golden']
    golden = bool(int(golden))

    response_data = {}

    profile = UserProfile.objects.get (user=user)

    maskItem = MaskItem.objects.get (card=card)

    if golden:
        totalCost = maskItem.buy_cost * 2
    else:
        totalCost = maskItem.buy_cost

    if totalCost <= profile.dust:
        collection = Collection.objects.get (owner=user)
        try:
            collectionItem = CollectionItem.objects.get (card=card, owner=collection.owner, golden=golden)
            collectionItem.count = collectionItem.count + 1
            collectionItem.save()

        except CollectionItem.DoesNotExist:
             collectionItem = CollectionItem.objects.create(
                card = card,
                owner = collection.owner,
                count = 1,
                golden = golden,
                level = 1
             )
             CollectionCollector.objects.create(collection=collection, item=collectionItem)

        profile.dust = profile.dust - totalCost
        profile.save()

        response_data['success'] = True
        response_data['count'] = collectionItem.count
        response_data['golden'] = golden
        response_data['dust'] = profile.dust

    else:
        response_data['success'] = False

    return HttpResponse(json.dumps(response_data), content_type="application/json")




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

        heroes = UserHero.objects.filter(owner=user)
        if len(heroes) == 0:
            hero = Hero.objects.get(vocation='adventurer')
            UserHero.objects.create(owner=user, hero=hero)

        try:
            collection = Collection.objects.get (owner=user)
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

        response_data['books'] = []
        books = {}

        items = collection.items.all().order_by('card__price')
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

            maskItem = MaskItem.objects.get (card=item.card)
            itemData['buy_cost'] = maskItem.buy_cost
            itemData['sale_cost'] = maskItem.sale_cost
            itemData['rarity'] = maskItem.rarity
            itemData['access_simple'] = maskItem.access_simple
            itemData['max_simple'] = maskItem.max_simple
            itemData['access_golden'] = maskItem.access_golden
            itemData['max_golden'] = maskItem.max_golden
            itemData['craft_available'] = maskItem.craft_available


            books[book_id]['cards'].append (itemData)

        for book in books:
            response_data['books'].append (books[book])


        initDecks (user, response_data)
        response_data['status'] = 'success'
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def getFullCollection (request):
    id = request.GET['user_id']
    user = User.objects.get(id=id)
    collection = Collection.objects.get (owner=user)

    updateCollection(user, collection)

    books = Book.objects.all()
    response_data = {}
    response_data['books'] = []

    profile = UserProfile.objects.get (user=user)
    response_data['dust'] = profile.dust

    for book in books:
         try:
              mask = BookMask.objects.get(book=book)
              bookData = {}
              bookData['id'] = book.id
              bookData['title'] = book.title
              bookData['description'] = book.description
              cards = []
              bookData['cards'] = cards
              for item in mask.items.all().order_by('card__price'):
                  card = item.card
                  cardData = {}
                  cardData['id'] =  card.id
                  cardData['price'] = card.price
                  cardData['title'] = card.title
                  cardData['description'] = card.description
                  cardData['attack'] = card.attack
                  cardData['health'] = card.health
                  cardData['type'] = card.type
                  cardData['buy_cost'] = item.buy_cost
                  cardData['sale_cost'] = item.sale_cost
                  cardData['rarity'] = item.rarity
                  cardData['access_simple'] = item.access_simple
                  cardData['max_simple'] = item.max_simple
                  cardData['access_golden'] = item.access_golden
                  cardData['max_golden'] = item.max_golden
                  cardData['craft_available'] = item.craft_available
                  try:
                      collectionItem = CollectionItem.objects.get (card=card, owner=user, golden=False)
                      cardData['simple_count'] = collectionItem.count
                  except CollectionItem.DoesNotExist:
                      cardData['simple_count'] = 0
                  try:
                      collectionItem = CollectionItem.objects.get (card=card, owner=user, golden=True)
                      cardData['golden_count'] = collectionItem.count
                  except CollectionItem.DoesNotExist:
                      cardData['golden_count'] = 0


                  cards.append(cardData)
              response_data['books'].append(bookData)
         except BookMask.DoesNotExist:
            pass

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

def updateCollection(user, collection):
    userHeroes = UserHero.objects.filter(owner=user)

    for userHero in userHeroes:
        hero = userHero.hero
        books = hero.book_set.all()

        for book in books:
            try:
                mask = BookMask.objects.get(book=book)
                updateByMask (mask, collection)
            except BookMask.DoesNotExist:
                pass

def updateByMask (mask, collection):
     for item in mask.items.all():
          if item.access_simple:
              try:
                  CollectionItem.objects.get(
                       card = item.card,
                       owner = collection.owner,
                       count = item.access_simple,
                       golden = False,
                       level = 1)
              except CollectionItem.DoesNotExist:
                  collectionItem = CollectionItem.objects.create(
                     card = item.card,
                     owner = collection.owner,
                     count = item.access_simple,
                     golden = False,
                     level = 1
                  )
                  CollectionCollector.objects.create(collection=collection, item=collectionItem)
          if item.access_golden:
               try:
                  CollectionItem.objects.get(
                       card = item.card,
                       owner = collection.owner,
                       count = item.access_golden,
                       golden = True,
                       level = 1)
               except CollectionItem.DoesNotExist:
                  collectionItem = CollectionItem.objects.create(
                     card = item.card,
                     owner = collection.owner,
                     count = item.access_golden,
                     golden = True,
                     level = 1
                  )
                  CollectionCollector.objects.create(collection=collection, item=collectionItem)

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

    #2 Содлат златоземья (id:166)
    card = Card.objects.get(id=166)
    create_deck_item(user, card, deck, 2)

    #3 Знахарь вуду (id:157)
    card = Card.objects.get(id=157)
    create_deck_item(user, card, deck, 2)

    #4 Ящер кровавой топи (id:204)
    card = Card.objects.get(id=204)
    create_deck_item(user, card, deck, 2)

    #5 Инженер новичек (id:184)
    card = Card.objects.get(id=184)
    create_deck_item(user, card, deck, 2)

    #6 Дворф диверсант (id:152)
    card = Card.objects.get(id=152)
    create_deck_item(user, card, deck, 2)

    #7 Охотница на иглошкурых (id:225)
    card = Card.objects.get(id=225)
    create_deck_item(user, card, deck, 2)

    #8 Лидер рейда (id:220)
    card = Card.objects.get(id=220)
    create_deck_item(user, card, deck, 2)

    #9 Гризли сталемех (id:218)
    card = Card.objects.get(id=218)
    create_deck_item(user, card, deck, 2)

    #10 Щитоносец Сен'джин (id:246)
    card = Card.objects.get(id=246)
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













