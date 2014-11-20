__author__ = 'inozemcev'

from card.models import Deck, Card
from hero.models import UserHero
from random import shuffle
import json
import math


from utils.timer_util import RenewableTimer


import logging
logger =  logging.getLogger('game_handler')


class Game ():

    def __init__(self, id):
        self.id = id
        self.player1Flag = False
        self.player2Flag = False
        self.whiteFlag = False

        self.whitePreflopFlag = False
        self.blackPreflopFlag = False
        self.blockEndPreflop = False

        self.white_ready = False
        self.black_ready = False

        self.white_price = 0
        self.black_price = 0


    def setPlayer1_id(self, id):
        self.p1_id = int(id)

    def getPlayer1_id(self):
        return  self.p1_id

    def setPlayer2_id(self, id):
        self.p2_id = int(id)

    def getPlayer2_id(self):
        return  self.p2_id

    def setPlayer1_level (self, lvl):
        self.player1_level = int(lvl)

    def setPlayer2_level(self, lvl):
        self.player2_level = int(lvl)

    def getPlayer1_level(self):
        return self.player1_level

    def getPlayer2_level(self):
        return self.player2_level

    def setWhiteHeroLevel (self, lvl):
        self.whiteHero_lvl = lvl

    def getWhiteHeroLevel (self):
        return self.whiteHero_lvl

    def setBlackHeroLevel (self, lvl):
        self.blackHero_lvl = lvl

    def getBlackHeroLevel (self):
        return self.blackHero_lvl

    def setPlayer1_deck(self, deckId):
        self.player1_deck = Deck.objects.get (id=deckId)

    def getPlayer1_deck (self):
        return self.player1_deck

    def setWhiteDeck (self, deck):
        self.white_deck = deck

    def setPlayer2_deck(self, deckId):
        self.player2_deck = Deck.objects.get (id=deckId)

    def getPlayer2_deck (self):
        return self.player2_deck

    def setBlackDeck (self, deck):
        self.black_deck = deck

    def setPlayer1_hero(self, heroId):
        self.player1_hero = UserHero.objects.get (id=heroId)

    def setPlayer2_hero(self, heroId):
        self.player2_hero = UserHero.objects.get (id=heroId)

    def getPlayer1_hero(self):
        return self.player1_hero

    def getPlayer2_hero(self):
        return self.player2_hero

    def setWhiteHero (self, hero):
        self.white_hero = hero

    def getWhiteHero (self):
        return self.white_hero

    def setBlackHero (self, hero):
        self.black_hero = hero

    def getBlackHero (self):
        return self.black_hero

    def setMode(self, md):
        self.mode = int(md)

    def getMode (self):
        return self.mode

    def setPlayer1 (self, player):
        self.player1Flag = True
        self.player1 = player

    def getPlayer1 (self):
        return self.player1

    def setPlayer2 (self, player):
        self.player2Flag = True
        self.player2 = player

    def getPlayer2 (self):
        return self.player2

    def setWhite (self, player):
        self.white = player

    def getWhite (self):
        return self.white

    def setBlack (self, player):
        self.black = player

    def getBlack (self):
        return self.black

    def setWhiteId (self, id):
        self.white_id = id

    def getWhiteId (self):
        return self.white_id

    def setBlackId (self, id):
        self.black_id = id

    def getBlackId (self):
        return self.black_id

    def getWhiteHand (self):
        return self.white_hand

    def getBlackHand (self):
        return self.black_hand

    def allPlayersInit (self):
        bool = False
        if self.player1Flag == True and self.player2Flag == True:
            bool = True

        return bool

    def generateHeroesHealth(self):
        self.whiteHealth = 30 + math.floor(self.whiteHero_lvl / 3)
        self.blackHealth = 30 + math.floor(self.blackHero_lvl / 3)

    def getWhiteHeroHealth(self):
        return self.whiteHealth

    def getBlackHeroHealth(self):
        return self.blackHealth

    def whiteReady(self):
        self.white_ready = True

    def blackReady(self):
        self.black_ready = True

    def isReady(self):
        if self.white_ready and self.black_ready:
            return True
        return False

    def generateMatchDecks (self):
        self.white_match_deck = []
        self.black_match_deck = []

        white_deck_items = self.white_deck.items.all()
        black_deck_items = self.black_deck.items.all()

        for item in white_deck_items:
            card = item.card
            cardData = dict()
            cardData['title'] = card.title
            cardData['description'] = card.description
            cardData['price'] = card.price
            cardData['health'] = card.health
            cardData['attack'] = card.attack
            cardData['id'] = card.id
            self.white_match_deck.append(cardData)

        shuffle(self.white_match_deck)

        for item in black_deck_items:
            card = item.card
            cardData = dict()
            cardData['title'] = card.title
            cardData['description'] = card.description
            cardData['price'] = card.price
            cardData['health'] = card.health
            cardData['attack'] = card.attack
            cardData['id'] = card.id
            self.black_match_deck.append(cardData)

        shuffle(self.black_match_deck)

    def generateHand (self, index, whiteFlag):
        if whiteFlag:
            self.white_hand = self.white_match_deck[:index]
            self.white_match_deck[:index] = []
            return self.white_hand
        else:
            self.black_hand = self.black_match_deck[:index]
            self.black_match_deck[:index] = []
            return self.black_hand


    def changePreflop (self, cards, whiteFlag):
        response = []
        if whiteFlag:
            for item in cards:
                card = Card.objects.get (id=int(item['id']))
                cardData = dict()
                cardData['title'] = card.title
                cardData['description'] = card.description
                cardData['price'] = card.price
                cardData['health'] = card.health
                cardData['attack'] = card.attack
                cardData['id'] = card.id
                self.white_match_deck.append(cardData)

            shuffle(self.white_match_deck)
            length = len(cards)

            response = self.white_match_deck[:length]
            self.white_match_deck[:length] = []

            i = 0
            for cardData in response:
                index = int(cards[i]['index'])
                self.white_hand[index] = cardData
                i += 1

            hand = []
            for data in self.white_hand:
                hand.append(data['price'])

            logger.debug(hand)

            self.whitePreflopFlag = True


        else:
            for item in cards:
                card = Card.objects.get (id=int(item['id']))
                cardData = dict()
                cardData['title'] = card.title
                cardData['description'] = card.description
                cardData['price'] = card.price
                cardData['health'] = card.health
                cardData['attack'] = card.attack
                cardData['id'] = card.id
                self.black_match_deck.append(cardData)

            shuffle(self.black_match_deck)
            length = len(cards)
            response = self.black_match_deck[:length]
            self.black_match_deck[:length] = []

            i = 0
            for cardData in response:
                index = int(cards[i]['index'])
                self.black_hand[index] = cardData
                i += 1

            hand = []
            for data in self.black_hand:
                hand.append(data['price'])

            logger.debug(hand)

            self.blackPreflopFlag = True

        return response

    def getWhiteCard(self):
        self.play_card = self.white_match_deck[:1][0]
        self.white_match_deck[:1] = []
        self.white_hand.append(self.play_card)
        logger.debug(self.play_card)
        return self.play_card


    def runPreflopTimer (self):
        self.preflop_timer = RenewableTimer(30, self.end_preflop_timer)
        self.preflop_timer.start()

    def isBlockEndPreflop (self):
        return self.blockEndPreflop

    def end_preflop_timer(self):
        
        if self.blockEndPreflop:
            return

        logger.debug('end_preflop_timer')
        response = {}
        response['status'] = 'success'
        response['type'] = 'end_preflop'

        data = {}
        data['preflop'] = self.white_hand
        response['data'] = data
        dump = json.dumps(response)
        self.white.write_message(dump)

        data = {}
        data['preflop'] = self.black_hand
        response['data'] = data
        dump = json.dumps(response)
        self.black.write_message(dump)

    def isAllPlayersChangePreflop(self):
        if self.whitePreflopFlag and self.blackPreflopFlag:
            return True

        return False

    def stopPreflopTimer (self) :
         self.preflop_timer.cancel()

    def incrementWhitePrice (self):
        if self.white_price < 10:
            self.white_price += 1

    def incrementBlackPrice (self):
        if self.black_price < 10:
            self.black_price += 1

    def getWhitePrice(self):
        return self.white_price

    def getBlackPrice(self):
        return self.black_price







