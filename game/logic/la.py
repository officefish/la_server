__author__ = 'inozemcev'

from card.models import Deck
from hero.models import UserHero
from random import randrange
from random import shuffle

import logging
logger =  logging.getLogger('game_handler')


class Game ():

    def __init__(self, id):
        self.id = id
        self.player1Flag = False
        self.player2Flag = False
        self.whiteFlag = False


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

    def setPlayer1_deck(self, deckId):
        self.player1_deck = Deck.objects.get (id=deckId)

    def setPlayer2_deck(self, deckId):
        self.player2_deck = Deck.objects.get (id=deckId)

    def setPlayer1_hero(self, heroId):
        self.player1_hero = UserHero.objects.get (id=heroId)

    def setPlayer2_hero(self, heroId):
        self.player2_hero = UserHero.objects.get (id=heroId)

    def setMode(self, md):
        self.mode = int(md)

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

    def allPlayersInit (self):
        bool = False
        if self.player1Flag == True and self.player2Flag == True:
            bool = True

        return bool

    def generateMatchDecks (self):
        self.player1_match_deck = []
        self.player2_match_deck = []

        player1_deck_items = self.player1_deck.items.all()
        player2_deck_items = self.player1_deck.items.all()

        for item in player1_deck_items:
            card = item.card
            cardData = dict()
            cardData['title'] = card.title
            cardData['description'] = card.description
            cardData['price'] = card.price
            cardData['health'] = card.health
            cardData['attack'] = card.attack
            cardData['id'] = randrange(1,500000)
            self.player1_match_deck.append(cardData)

        shuffle(self.player1_match_deck)

        logger.debug(self.player1_match_deck)

        for item in player2_deck_items:
            card = item.card
            cardData = dict()
            cardData['title'] = card.title
            cardData['description'] = card.description
            cardData['price'] = card.price
            cardData['health'] = card.health
            cardData['attack'] = card.attack
            cardData['id'] = randrange(1,500000)
            self.player2_match_deck.append(cardData)

        shuffle(self.player2_match_deck)

    def getPreflop (self, index, player):
        if player == 1:
            l = self.player1_match_deck[:index]
            self.player1_match_deck[:index] = []
            return l
        else:
            l = self.player2_match_deck[:index]
            self.player2_match_deck[:index] = []
            return l



