__author__ = 'inozemcev'

from card.models import Deck, Card
from hero.models import UserHero
from random import shuffle
import json
import math
import random

from game.logic.constants import EptitudeLevel, EptitudeAttachment, EptitudeCondition, EptitudePeriod, CardType, EptitudeType
from game.logic.controller import Controller
from game.logic.cardController import CardController
from game.logic.action import Action
from game.logic.unit import Unit, HeroUnit, UnitEptitude

from card.models import Race, SubRace
from group.models import Group

from utils.timer_util import RenewableTimer


import logging
logger =  logging.getLogger('game_handler')


class Game ():

    def __init__(self, id):
        self.id = id
        self.player1Flag = False
        self.player2Flag = False
        self.stepFlag = False

        self.whitePreflopFlag = False
        self.blackPreflopFlag = False
        self.blockEndPreflop = False

        self.white_ready = False
        self.black_ready = False

        self.white_price = 0
        self.black_price = 0

        self.white_step_price = 0
        self.black_step_price = 0

        self.whiteUnitRow = []
        self.blackUnitRow = []

        self.selectMode = False

        self.whiteSpellMixin = 0
        self.blackSpellMixin = 0

        self.dieUnitsIndex = 0

        self.seriesFlag = False

        self.whiteOverload = 0
        self.blackOverload = 0

        self.stepOverload = 0

        self.burnExtraCardsFlag = True
        self.attritionFlag = True

        self.whiteAttritionIndex = 0
        self.blackAttritionIndex = 0


    def transitionProgress (self):
        if self.stepFlag:
            self.stepFlag = False
        else:
            self.stepFlag = True
        logger.debug ('stepFlag: %s' % self.stepFlag)



    def getStepFlag (self):
        return self.stepFlag

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

    def generateHeroesUnits(self):
        self.whiteHeroUnit = HeroUnit(self.whiteHealth)
        self.whiteHeroUnit.whiteFlag = True
        self.blackHeroUnit = HeroUnit(self.blackHealth)
        self.blackHeroUnit.whiteFlag = False

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

    def getPlayerLastCard(self, whiteFlag):
        if whiteFlag:
            card = self.lastWhiteCard
        else:
            card = self.lastBlackCard
        return card

    def getOpponentLastCard(self, whiteFlag):
        if whiteFlag:
            card = self.lastBlackCard
        else:
            card = self.lastWhiteCard
        return card

    def configureLastCard (self, card):
        self.lastCardinHand = card
        try:
            self.white_hand.index(card)
            self.lastWhiteCard = card
        except:
            pass

        try:
            self.black_hand.index(card)
            self.lastBlackCard = card
        except:
            pass

    def generateMatchDecks (self):
        self.white_match_deck = []
        self.black_match_deck = []

        white_deck_items = self.white_deck.items.all()
        black_deck_items = self.black_deck.items.all()

        for item in white_deck_items:
            card = item.collectionItem.card
            cardData = self.getUnitCardData(card)
            self.white_match_deck.append(cardData)

        shuffle(self.white_match_deck)

        for item in black_deck_items:
            card = item.collectionItem.card
            cardData = self.getUnitCardData(card)
            self.black_match_deck.append(cardData)

        shuffle(self.black_match_deck)

    def generateHand (self, index, whiteFlag):
        if whiteFlag:
            self.white_hand = self.white_match_deck[:index]
            self.white_match_deck[:index] = []
            for card in self.white_hand:
                card['whiteFlag'] = True

            return self.white_hand
        else:
            self.black_hand = self.black_match_deck[:index]
            self.black_match_deck[:index] = []
            for card in self.black_hand:
                card['whiteFlag'] = False

            return self.black_hand




    def changePreflop (self, cards, whiteFlag):
        response = []
        if whiteFlag:
            for item in cards:
                card = Card.objects.get (id=int(item['id']))
                cardData = self.getUnitCardData(card)
                self.white_match_deck.append(cardData)

            shuffle(self.white_match_deck)
            length = len(cards)

            response = self.white_match_deck[:length]
            self.white_match_deck[:length] = []

            i = 0
            for cardData in response:
                index = int(cards[i]['index'])
                cardData['whiteFlag'] = True
                self.white_hand[index] = cardData
                i += 1


            self.whitePreflopFlag = True


        else:
            for item in cards:
                card = Card.objects.get (id=int(item['id']))
                cardData = self.getUnitCardData(card)
                self.black_match_deck.append(cardData)

            shuffle(self.black_match_deck)
            length = len(cards)
            response = self.black_match_deck[:length]
            self.black_match_deck[:length] = []

            i = 0
            for cardData in response:
                index = int(cards[i]['index'])
                cardData['whiteFlag'] = False
                self.black_hand[index] = cardData
                i += 1



            self.blackPreflopFlag = True

        return response

    def getCardById(self, id):
        try:
            card = Card.objects.get(id=id)
        except Card.DoesNotExist:
            card = None
        return  card

    def getUnitCardData (self, card):
        cardData = dict()
        cardData['title'] = card.title
        cardData['description'] = card.description
        cardData['price'] = card.price
        cardData['defaultPrice'] = card.price
        cardData['priceMixin'] = 0
        cardData['health'] = card.health
        cardData['attack'] = card.attack
        cardData['id'] = card.id
        cardData['uid'] = random.randint(0, 1000000)
        cardData['type'] = card.type
        cardData['widget'] = card.widget
        try:
            cardData['group'] = card.group.title
            cardData['groupId'] = card.group.id
        except:
            pass
        try:
            cardData['race'] = card.race.title
            cardData['raceId'] = card.race.id
        except:
            pass
        try:
            cardData['subrace'] = card.subrace.title
        except:
            pass
        dataEptitudes = []
        for eptitude in card.eptitudes:
            dataEptitude = self.getEptitudeData (eptitude)
            dataEptitudes.append (dataEptitude)
        cardData['eptitudes'] = dataEptitudes
        return cardData

    def getEptitudeData (self, eptitude):
        eptitudeData = dict ()
        eptitudeData['type'] = eptitude.type
        eptitudeData['period'] = eptitude.period
        eptitudeData['level'] = eptitude.level
        eptitudeData['power'] = eptitude.power
        eptitudeData['max_power'] = eptitude.max_power
        eptitudeData['count'] = eptitude.count
        eptitudeData['lifecycle'] = eptitude.lifecycle
        eptitudeData['attachment'] = eptitude.attachment
        eptitudeData['attach_hero'] = eptitude.attach_hero
        eptitudeData['attach_initiator'] = eptitude.attach_initiator
        eptitudeData['dynamic'] = eptitude.dynamic
        eptitudeData['condition'] = eptitude.condition
        if eptitude.spellCondition:
            logger.debug('init eptitude.spellCondition:%s' % eptitude.spellCondition)
        eptitudeData['spellCondition'] = eptitude.spellCondition
        eptitudeData['id'] = eptitude.id
        eptitudeData['battlecry'] = eptitude.battlecry
        eptitudeData['price'] = eptitude.price
        eptitudeData['probability'] = eptitude.probability
        eptitudeData['spellSensibility'] = eptitude.spellSensibility
        try:
            eptitudeData['dependency'] = eptitude.dependency.id
        except:
            eptitudeData['dependency'] = 0

        try:
            eptitudeData['attach_eptitude'] = eptitude.attach_eptitude.id
        except:
            eptitudeData['attach_eptitude'] = 0

        try:
            eptitudeData['race'] = eptitude.race.id
        except: pass
        try:
            eptitudeData['subrace'] = eptitude.subrace.id
        except: pass
        try:
            eptitudeData['unit'] = eptitude.unit.id
        except: pass
        try:
            eptitudeData['group'] = eptitude.group.id
        except:
            pass
        return eptitudeData

    def isBlockEndPreflop (self):
        return self.blockEndPreflop

    def isAllPlayersChangePreflop(self):
        if self.whitePreflopFlag and self.blackPreflopFlag:
            return True

        return False


    def runPreflopTimer (self):
        self.preflop_timer = RenewableTimer(30, self.end_preflop_timer)
        self.preflop_timer.start()

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

    def stopPreflopTimer (self) :
         self.preflop_timer.cancel()

    def runStepTimer (self):
        try:
            self.step_timer.pause()
            del self.step_timer
        except:
            pass

        try:
            self.step_finish_timer.pause()
            del self.step_finish_timer
        except:
            pass

        logger.debug ('run_step_timer')
        self.step_timer = RenewableTimer(20, self.end_step_timer)
        self.step_timer.start()

    def end_step_timer(self):

        logger.debug('end_step_timer')
        response = {}
        response['status'] = 'success'
        response['type'] = 'end_step_timer'
        dump = json.dumps(response)
        self.white.write_message(dump)
        self.black.write_message(dump)

        self.step_finish_timer = RenewableTimer(15, self.end_step_finish_timer)
        self.step_finish_timer.start()
        logger.debug('run step_finish_timer')

    def end_step_finish_timer (self):
        logger.debug ('end_step_finish_timer')

        prevWhiteFlag = self.getStepFlag()
        scenario = self.endStep()

        whiteFlag = self.getStepFlag()
        if whiteFlag:
            hand = self.black_hand
            row = self.blackUnitRow
            client = self.getBlackId()

        else:
            hand = self.white_hand
            row = self.whiteUnitRow
            client = self.getWhiteId()

        if  self.selectMode:

            cardData = self.selected_unit.cardData
            hand.append (cardData)
            selectAttachment = self.initAttachment (self.selected_unit, prevWhiteFlag)
            selectIndex = self.initIndex (self.selected_unit, selectAttachment, prevWhiteFlag)
            del row[selectIndex]

            action = {}
            action['targetIndex'] = selectIndex
            action['targetAttachment'] = selectAttachment
            action['type'] = Action.BACK_TOKEN_TO_HAND
            action['client'] = client
            action['endAnimationFlag'] = True
            action['card'] = cardData
            action['opponent_ignore'] = True
            scenario.insert(0, action)

            action = {}
            action['type'] = Action.STOP_SELECT_MODE
            action['client'] = client
            action['endAnimationFlag'] = True
            scenario.insert(0, action)

            self.selectMode = False

        response = {}
        response['status'] = 'success'
        response['type'] = 'scenario'
        data = {}
        data['scenario'] = scenario
        response['data'] = data
        dump = json.dumps(response)
        self.getWhite().write_message(dump)
        self.getBlack().write_message(dump)

    def calculateCards(self, client, scenario, whiteFlag):
        if whiteFlag:
            deck = self.white_match_deck
            opponentDeck = self.black_match_deck
        else:
            deck = self.black_match_deck
            opponentDeck = self.white_match_deck

        action = {}
        action['type'] = Action.CALCULATE_CARDS
        action['client'] = client
        action['clientCardsCount'] = len(deck)
        action['opponentCardsCount'] = len(opponentDeck)
        scenario.append(action)


    def getCard(self, whiteFlag, appendFlag):
        if whiteFlag:
             play_card = self.white_match_deck[:1][0]
             self.white_match_deck[:1] = []
             if appendFlag:
                 self.play_card = play_card
                 self.white_hand.append(self.play_card)
                 self.play_card['whiteFlag'] = True
        else:
             play_card = self.black_match_deck[:1][0]
             self.black_match_deck[:1] = []
             if appendFlag:
                 self.play_card = play_card
                 self.black_hand.append(self.play_card)
                 self.play_card['whiteFlag'] = False

        logger.debug(play_card)
        return play_card

    def getCardByIndex (self, index, whiteFlag):
        if whiteFlag:
            deck = self.white_match_deck
        else:
            deck = self.black_match_deck
        card = deck[index]
        card['whiteFlag'] = whiteFlag
        del deck[index]
        return  card



    def getUnitCardsList (self, whiteFlag):
        cardsList = []

        if whiteFlag:
            deck = self.white_match_deck
        else:
            deck = self.black_match_deck

        for card in deck:
            if card['type'] == CardType.UNIT:
                cardsList.append(card)

        return cardsList

    def getUnitCardsHandList (self, whiteFlag):
        cardsList = []

        if whiteFlag:
            hand = self.white_hand
        else:
            hand = self.black_hand

        for card in hand:
            if card['type'] == CardType.UNIT:
                cardsList.append(card)

        return cardsList



    def incrementPrice (self, whiteFlag):
        if whiteFlag:
            if self.white_price < 10:
                self.white_price += 1
        else:
            if self.black_price < 10:
                self.black_price += 1

    def getPrice(self, whiteFlag):
        if whiteFlag:
            return self.white_price
        else:
            return self.black_price

    def initStepPrice (self):
        self.white_step_price = self.white_price
        self.black_step_price = self.black_price


    def getStepPrice (self, whiteFlag):
        if whiteFlag:
            return self.white_step_price
        else:
            return self.black_step_price

    def getRowLength (self, whiteFlag):
        if whiteFlag:
            return len(self.whiteUnitRow)
        else:
            return len(self.blackUnitRow)

    def deleteUnit (self, index, attachment, whiteFlag):
        if whiteFlag:
            row = self.whiteUnitRow
            opponentRow = self.blackUnitRow
        else:
            row = self.blackUnitRow
            opponentRow = self.whiteUnitRow

        if attachment:
            target = row[index]
            target.setIndex(index)
            target.setWhiteFlag(whiteFlag)
            target.setRow (row)
            del row[index]
        else:
            target = opponentRow[index]
            target.setIndex(index)
            target.setRow(opponentRow)
            del opponentRow[index]

    def endMatch(self, client, scenario, whiteFlag):
        try:
            self.step_timer.pause()
            del self.step_timer
        except:
            pass
        try:
            self.step_finish_timer.pause()
            del self.step_finish_timer
        except:
            pass

        playerWinFlag = False
        opponentWinFlag = False

        if whiteFlag:
            hero = self.whiteHeroUnit
            opponentHero = self.blackHeroUnit
        else:
            hero = self.blackHeroUnit
            opponentHero = self.whiteHeroUnit

        if hero.getHealth() > 0:
            playerWinFlag = True

        if opponentHero.getHealth() > 0:
            opponentWinFlag = True

        action = {}
        action['type'] = Action.END_MATCH
        action['client'] = client
        action['playerWin'] = playerWinFlag
        action['opponentWin'] = opponentWinFlag
        scenario.append(action)



    def start(self):

        self.incrementPrice(True)
        self.initStepPrice ()
        self.transitionProgress ()

        card = self.getCard(True, True)
        client = self.getWhiteId()
        price = self.getStepPrice(True)

        self.scenario = []

        action = {}
        action['type'] = Action.STEP_PRICE
        action['client'] = client
        action['price'] = price
        action['overload'] = self.stepOverload
        action['endAnimationFlag'] = False
        self.scenario.append (action)

        action = {}
        action['type'] = Action.SORT_DECK
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

        action = {}
        action['type'] = Action.PICK_CARD
        action['client'] = client
        action['attachment'] = EptitudeAttachment.ASSOCIATE
        action['card'] = card
        action['endAnimationFlag'] = True
        self.scenario.append(action)

        self.calculateCards(client, self.scenario, True)

        action = {}
        action['type'] = Action.STEP
        action['client'] = client
        self.scenario.append(action)

        action = {}
        action['type'] = Action.UNBLOCK_DECK
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

        action = {}
        action['type'] = Action.GLOW_CARDS
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

        controller = CardController()
        controller.setWhiteFlag(True)
        controller.setMatch(self)
        controller.setScenario(self.scenario)
        controller.setClient(client)
        controller.new_card()

        #self.runStepTimer()
        return self.scenario

    def endStep (self):

        self.scenario = []

        whiteFlag = self.getStepFlag()

        self.stepOverload = 0

        if whiteFlag:
            row = self.whiteUnitRow
            client = self.getWhiteId()
            opponentRow = self.blackUnitRow
        else:
            row = self.blackUnitRow
            client = self.getBlackId()
            opponentRow = self.whiteUnitRow

        action = {}
        action['type'] = Action.END_STEP
        action['client'] = client
        self.scenario.append (action)

        self.seriesFlag = False
        action = {}
        action['type'] = Action.DEACTIVATE_DRAWING_SERIES
        action['client'] = client
        self.scenario.append(action)

        for unit in row:
            self.controller = Controller()
            self.controller.setMatch(self)
            self.controller.setScenario(self.scenario)
            self.controller.setClient(client)
            self.controller.setWhiteFlag(whiteFlag)
            self.controller.endStep(unit)
            if unit.containsTempEptitudes():
                self.controller.deactivateTempEptitudes(unit)

        for unit in opponentRow:
            self.controller = Controller()
            self.controller.setMatch(self)
            self.controller.setScenario(self.scenario)
            self.controller.setClient(client)
            self.controller.setWhiteFlag(whiteFlag)
            self.controller.opponentEndStep(unit)

            if unit.containsTempEptitudes():
                self.controller.deactivateTempEptitudes(unit)

        if self.whiteHeroUnit.containsTempEptitudes():
            self.controller.deactivateTempEptitudes(self.whiteHeroUnit)

        if self.blackHeroUnit.containsTempEptitudes():
            self.controller.deactivateTempEptitudes(self.blackHeroUnit)

        self.transitionProgress ()

        whiteFlag = self.getStepFlag()

        if whiteFlag:
            row = self.whiteUnitRow
            opponentRow = self.blackUnitRow
            client = self.getWhiteId()
            hero = self.whiteHeroUnit
            hand = self.white_hand

        else:
            row = self.blackUnitRow
            opponentRow = self.whiteUnitRow
            client = self.getBlackId()
            hero = self.blackHeroUnit
            hand = self.black_hand

        self.activePlayer = hero

        if hero.freeze:
             hero.freezeIndex -= 1
             if hero.freezeIndex <= 0:
                 hero.freezeIndex = 0
                 hero.freeze = False
                 self.destroyFreeze(hero, client, self.scenario)

        action = {}
        action['type'] = Action.STOP_STEP_TIMER
        self.scenario.append (action)

        self.incrementPrice(whiteFlag)
        self.initStepPrice ()
        price = self.getStepPrice(whiteFlag)

        if whiteFlag:
            if self.whiteOverload > 0:
                self.white_step_price -= self.whiteOverload
                price = self.white_step_price
                self.stepOverload = self.whiteOverload
                self.whiteOverload = 0

                action = {}
                action['type'] = Action.CLEAR_OVERLOAD
                action['client'] = client
                action['endAnimationFlag'] = False
                self.scenario.append (action)

        else:
             if self.blackOverload > 0:
                self.black_step_price -= self.blackOverload
                price = self.black_step_price
                self.stepOverload = self.blackOverload
                self.blackOverload = 0

                action = {}
                action['type'] = Action.CLEAR_OVERLOAD
                action['client'] = client
                action['endAnimationFlag'] = False
                self.scenario.append (action)

        action = {}
        action['type'] = Action.STEP_PRICE
        action['client'] = client
        action['price'] = price
        action['overload'] = self.stepOverload
        action['endAnimationFlag'] = False
        self.scenario.append (action)

        action = {}
        action['type'] = Action.SORT_DECK
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

        for unit in row:
            self.controller = Controller()
            self.controller.setMatch(self)
            self.controller.setScenario(self.scenario)
            self.controller.setClient(client)
            self.controller.setWhiteFlag(whiteFlag)
            self.controller.startStep(unit)

        for unit in opponentRow:
            self.controller = Controller()
            self.controller.setMatch(self)
            self.controller.setScenario(self.scenario)
            self.controller.setClient(client)
            self.controller.setWhiteFlag(whiteFlag)
            self.controller.opponentStartStep(unit)

        if self.deckLength(whiteFlag):

            if len(hand) < 10:
                card = self.getCard(whiteFlag, True)
                cardCopy = self.copyCard(card)
                action = {}
                action['type'] = Action.PICK_CARD
                action['client'] = client
                action['attachment'] = EptitudeAttachment.ASSOCIATE
                action['card'] = cardCopy
                action['endAnimationFlag'] = True
                self.scenario.append(action)

                logger.debug('attachment:%s' % action['attachment'])

                self.lastCardinHand = card
                if whiteFlag:
                    self.lastWhiteCard = card
                else:
                    self.lastBlackCard = card

                for unit in row:
                    self.controller = Controller()
                    self.controller.setMatch(self)
                    self.controller.setScenario(self.scenario)
                    self.controller.setClient(client)
                    self.controller.setWhiteFlag(whiteFlag)
                    self.controller.newCard(unit)
                    self.controller.newPlayerCard(unit)

                for unit in opponentRow:
                    self.controller = Controller()
                    self.controller.setMatch(self)
                    self.controller.setScenario(self.scenario)
                    self.controller.setClient(client)
                    self.controller.setWhiteFlag(whiteFlag)
                    self.controller.newCard(unit)
                    self.controller.newOpponentCard(unit)


            else:
                if self.burnExtraCardsFlag:
                    logger.debug('BURN_CARD')
                    card = self.getCard(whiteFlag, False)
                    cardCopy = self.copyCard(card)
                    action = {}
                    action['type'] = Action.BURN_CARD
                    action['attachment'] = EptitudeAttachment.ASSOCIATE
                    action['client'] = client
                    action['card'] = cardCopy
                    action['endAnimationFlag'] = True
                    self.scenario.append(action)

        else:
            if self.attritionFlag:
                self.attrition(client, whiteFlag)

        self.calculateCards(client, self.scenario, whiteFlag)

        action = {}
        action['type'] = Action.STEP
        action['client'] = client
        self.scenario.append(action)

        action = {}
        action['type'] = Action.UNBLOCK_DECK
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

        action = {}
        action['type'] = Action.ATTACK_AVAILABLE
        action['client'] = client
        action['endAnimationFlag'] = False
        units = []
        for unit in row:
            unit.stepCount = unit.stepCount + 1
            if unit.freeze:
                unit.freezeIndex -= 1
                if unit.freezeIndex <= 0:
                    unit.freezeIndex = 0
                    unit.freeze = False
                    self.destroyFreeze(unit, client, self.scenario)

            if unit.canAttack and unit.attack > 0 and unit.freeze == False and unit.replaceFlag == False:
                if unit.doubleAttack:
                    unit.setStepAttack (2)
                else:
                    unit.setStepAttack (1)

                units.append (row.index(unit))

            if unit.replaceFlag:
                unit.replaceFlag = False

        action['unitList'] = units
        self.scenario.append(action)

        action = {}
        action['type'] = Action.GLOW_UNITS
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

        if len(row) < 7:
            action = {}
            action['type'] = Action.GLOW_CARDS
            action['client'] = client
            action['endAnimationFlag'] = False
            self.scenario.append(action)

        controller = CardController()
        controller.setWhiteFlag(whiteFlag)
        controller.setMatch(self)
        controller.setScenario(self.scenario)
        controller.setClient(client)
        controller.new_card()
        #self.runStepTimer()


        return self.scenario

    def deckLength(self, whiteFlag):
        if whiteFlag:
            return len(self.white_match_deck)
        else:
            return len(self.black_match_deck)

    def attrition (self, client, whiteFlag):
        if whiteFlag:
            hero = self.whiteHeroUnit
            self.whiteAttritionIndex += 1
            damage = self.whiteAttritionIndex
        else:
            hero = self.blackHeroUnit
            self.blackAttritionIndex += 1
            damage = self.blackAttritionIndex

        targetAttachment = self.initAttachment (hero, whiteFlag)
        targetIndex = self.initIndex (hero, targetAttachment, whiteFlag)

        action = {}
        action['type'] = Action.ATTRITION
        action['damage'] = damage
        self.scenario.append(action)

        action = {}
        action['type'] = Action.DAMAGE
        action['targets'] = [{'index':targetIndex, 'attachment':targetAttachment, 'damage':damage }]
        action['client'] = client
        self.scenario.append(action)

        targetNewHealthValue = hero.getHealth() - damage
        hero.setHealth(targetNewHealthValue)

        action = {}
        action['type'] = Action.HEALTH_AFTER_PASSIVE_ATTACK
        action['client'] = client
        action['endAnimationFlag'] = False
        action['targetIndex'] = targetIndex
        action['targetAttachment'] = targetAttachment
        action["targetUnitHealth"] = hero.getHealth()
        self.scenario.append(action)

        controller = CardController()
        controller.setWhiteFlag(whiteFlag)
        controller.setMatch(self)
        controller.setScenario(self.scenario)
        controller.setClient(client)
        controller.hero_wound(whiteFlag)

        if hero.getHealth() <=0:
            #logger.debug ('addAction::opponent_hero_death')
            self.endMatch(client, self.scenario, whiteFlag)





    def copyCard (self, card):
        cardData = dict()
        cardData['title'] = card['title']
        cardData['description'] = card['description']
        cardData['price'] = card['price']
        cardData['health'] = card['health']
        cardData['attack'] = card['attack']
        cardData['id'] = card['id']
        cardData['uid'] = random.randint(0, 1000000)
        cardData['type'] = card['type']
        cardData['priceMixin'] = card['priceMixin']
        cardData['widget'] = card['widget']
        try:
            cardData['race'] = card['race']
        except:
            pass
        try:
            cardData['subrace'] = card['subrace']
        except:
            pass
        try:
            cardData['group'] = card['group']
            cardData['groupId'] = card['groupId']
        except:
            pass
        cardData['eptitudes'] = card['eptitudes']
        return cardData


    def destroyFreeze (self, unit, client, scenario):
        attachment = self.initAttachment (unit, unit.whiteFlag)
        index = self.initIndex (unit, attachment, unit.whiteFlag)
        action = {}
        action['index'] = index
        action['attachment'] = attachment
        action['type'] = Action.DESTROY_FREEZE
        action['client'] = client
        action['endAnimationFlag'] = True
        scenario.append (action)

    def playSpell (self, cardIndex, whiteFlag):
        self.scenario = []

        if whiteFlag:
            cardData = self.white_hand[cardIndex]
            client = self.getWhiteId()
            hand = self.white_hand

            totalCardPrice = cardData['price'] + cardData['priceMixin']
            price = self.white_step_price - totalCardPrice
            hero = self.whiteHeroUnit

        else:
            cardData = self.black_hand[cardIndex]
            client = self.getBlackId()
            hand = self.black_hand

            totalCardPrice = cardData['price'] + cardData['priceMixin']
            price = self.black_step_price - totalCardPrice
            hero = self.blackHeroUnit

        if self.containsSelectEffectEptitude(cardData):
            logger.debug ('Spell contains SELECT_EFFECT eptitude')
            groupId = cardData['eptitudes'][0]['group']
            group = Group.objects.get(pk=groupId)
            cards = []

            for selectCard in group.cards:
                selectCardData = self.getUnitCardData (selectCard)
                selectCardData['whiteFlag'] = whiteFlag
                cards.append(selectCardData)

            action = {}
            action['type'] = Action.SELECT_EFFECT
            action['client'] = client
            action['cards'] = cards
            self.scenario.append (action)

            self.effectCards = cards
            self.effectCardIndex = cardIndex

            return

        hero.configureEptitudes(cardData)
        del hand[cardIndex]
        if whiteFlag:
            self.white_step_price = price
        else:
            self.black_step_price = price

        action = {}
        action['type'] = Action.STEP_PRICE
        action['client'] = client
        action['price'] = price
        action['overload'] = self.stepOverload
        action['endAnimationFlag'] = False
        self.scenario.append (action)

        action = {}
        action['type'] = Action.DESTROY_ACTUAL_CARD
        action['client'] = client
        action['endAnimationFlag'] = True
        action['cardIndex'] = cardIndex
        action['enemy'] = True
        self.scenario.append(action)

        action = {}
        action['type'] = Action.SORT_DECK
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

        self.controller = Controller()
        self.controller.setMatch(self)
        self.controller.setScenario(self.scenario)
        self.controller.setClient(client)
        self.controller.setWhiteFlag(whiteFlag)
        self.controller.spell(hero)

        hero.destroyEptitudes()

        if whiteFlag:
            row = self.whiteUnitRow
            opponentRow = self.blackUnitRow
        else:
            row = self.blackUnitRow
            opponentRow = self.whiteUnitRow

        for unit in row:
            self.controller.associateSpell(unit)
            self.controller.allSpell(unit)

        for unit in opponentRow:
            self.controller.opponentSpell(unit)
            self.controller.allSpell(unit)

        action = {}
        action['type'] = Action.UNBLOCK_DECK
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

        if not self.seriesFlag:
            self.seriesFlag = True
            action = {}
            action['type'] = Action.ACTIVATE_DRAWING_SERIES
            action['client'] = client
            self.scenario.append(action)

        action = {}
        action['type'] = Action.GLOW_CARDS
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

    def guise_selected (self, whiteFlag, index):
        self.scenario = []
        guiseCard =  self.guiseCards[index]
        guiseUnit = Unit(guiseCard)

        if whiteFlag:
            client = self.getWhiteId()
        else:
            client = self.getBlackId()


        self.controller = Controller()



        self.controller.setMatch(self)
        self.controller.setScenario(self.scenario)
        self.controller.setClient(client)
        self.controller.setWhiteFlag(whiteFlag)

        self.controller.configureUnit (guiseUnit)

        self.controller.unit = self.lastPlaced
        self.controller.copy_unit([guiseUnit], UnitEptitude())

        return self.scenario


    def effect_selected (self, whiteFlag, index):
        self.scenario = []
        self.effectCard =  self.effectCards[index]

        if whiteFlag:
            cardData = self.white_hand[self.effectCardIndex]
            client = self.getWhiteId()
            hand = self.white_hand
            totalCardPrice = cardData['price'] + cardData['priceMixin']
            price = self.white_step_price - totalCardPrice
            hero = self.whiteHeroUnit

        else:
            cardData = self.black_hand[self.effectCardIndex]
            client = self.getBlackId()
            hand = self.black_hand
            totalCardPrice = cardData['price'] + cardData['priceMixin']
            price = self.black_step_price - totalCardPrice

            hero = self.blackHeroUnit
        if self.effectCard['type'] == CardType.SPELL_TO_TARGET:
            action = {}
            action['type'] = Action.SELECT_FOR_EFFECT
            action['client'] = client
            action['endAnimationFlag'] = False
            self.scenario.append(action)

        if self.effectCard['type'] == CardType.SPELL:

            hero.configureEptitudes(self.effectCard)
            del hand[self.effectCardIndex]
            if whiteFlag:
                self.white_step_price = price
            else:
                self.black_step_price = price

            action = {}
            action['type'] = Action.STEP_PRICE
            action['client'] = client
            action['price'] = price
            action['overload'] = self.stepOverload
            action['endAnimationFlag'] = False
            self.scenario.append (action)

            action = {}
            action['type'] = Action.DESTROY_ACTUAL_CARD
            action['client'] = client
            action['enemy'] = True
            action['cardIndex'] = self.effectCardIndex
            action['endAnimationFlag'] = False
            self.scenario.append(action)

            action = {}
            action['type'] = Action.SORT_DECK
            action['client'] = client
            action['endAnimationFlag'] = False
            self.scenario.append(action)

            self.controller = Controller()
            self.controller.setMatch(self)
            self.controller.setScenario(self.scenario)
            self.controller.setClient(client)
            self.controller.setWhiteFlag(whiteFlag)
            self.controller.spell(hero)

            hero.destroyEptitudes()

            if whiteFlag:
                row = self.whiteUnitRow
                opponentRow = self.blackUnitRow
            else:
                row = self.blackUnitRow
                opponentRow = self.whiteUnitRow

            for unit in row:
                self.controller.associateSpell(unit)
                self.controller.allSpell(unit)

            for unit in opponentRow:
                self.controller.opponentSpell(unit)
                self.controller.allSpell(unit)

            action = {}
            action['type'] = Action.UNBLOCK_DECK
            action['client'] = client
            action['endAnimationFlag'] = False
            self.scenario.append(action)

            if not self.seriesFlag:
                self.seriesFlag = True
                action = {}
                action['type'] = Action.ACTIVATE_DRAWING_SERIES
                action['client'] = client
                self.scenario.append(action)

            action = {}
            action['type'] = Action.GLOW_CARDS
            action['client'] = client
            action['endAnimationFlag'] = False
            self.scenario.append(action)


        return self.scenario


    def containsSelectEffectEptitude (self, cardData):
        effect = False
        for eptitudeData in cardData['eptitudes']:
            if eptitudeData['type'] == EptitudeType.SELECT_EFFECT:
                effect = True
        return effect

    def spellToTarget(self, cardIndex, targetIndex, targetAttachment, whiteFlag):
        self.scenario = []

        if whiteFlag:
            cardData = self.white_hand[cardIndex]
            client = self.getWhiteId()

            hand = self.white_hand

            totalCardPrice = cardData['price'] + cardData['priceMixin']
            price = self.white_step_price - totalCardPrice

            hero = self.whiteHeroUnit

        else:
            cardData = self.black_hand[cardIndex]
            client = self.getBlackId()

            hand = self.black_hand

            totalCardPrice = cardData['price'] + cardData['priceMixin']
            price = self.black_step_price - totalCardPrice

            hero = self.blackHeroUnit


        self.spellTarget = self.getUnitByIndexAndAttachment(targetIndex, targetAttachment, whiteFlag)
        hero.configureEptitudes(cardData)

        valid = self.validateSpellTarget (hero, whiteFlag)

        if valid:
            if self.spellTarget.spellInvisible:
                logger.debug('spellTarget is spellInvisible')
                valid = False

        if valid:
            del hand[cardIndex]
            if whiteFlag:
                self.white_step_price = price
            else:
                self.black_step_price = price

            action = {}
            action['type'] = Action.STEP_PRICE
            action['client'] = client
            action['price'] = price
            action['overload'] = self.stepOverload
            action['endAnimationFlag'] = False
            self.scenario.append (action)

            action = {}
            action['type'] = Action.DESTROY_ACTUAL_CARD
            action['enemy'] = True
            action['client'] = client
            action['cardIndex'] = cardIndex
            action['endAnimationFlag'] = False
            self.scenario.append(action)

            action = {}
            action['type'] = Action.SORT_DECK
            action['client'] = client
            action['endAnimationFlag'] = False
            self.scenario.append(action)

            logger.debug ('hand length: %s' % len(hand))

            logger.debug('card title: %s' % cardData['title'])

            self.controller = Controller()
            self.controller.setMatch(self)
            self.controller.setScenario(self.scenario)
            self.controller.setClient(client)
            self.controller.setWhiteFlag(whiteFlag)
            self.controller.spellToTarget(hero)

            hero.destroyEptitudes()

            if whiteFlag:
                row = self.whiteUnitRow
                opponentRow = self.blackUnitRow
            else:
                row = self.blackUnitRow
                opponentRow = self.whiteUnitRow

            for unit in row:
                self.controller.associateSpell(unit)
                self.controller.allSpell(unit)

            for unit in opponentRow:
                self.controller.opponentSpell(unit)
                self.controller.allSpell(unit)

            action = {}
            action['type'] = Action.UNBLOCK_DECK
            action['client'] = client
            action['endAnimationFlag'] = False
            self.scenario.append(action)

            if not self.seriesFlag:
                self.seriesFlag = True
                action = {}
                action['type'] = Action.ACTIVATE_DRAWING_SERIES
                action['client'] = client
                self.scenario.append(action)

            action = {}
            action['type'] = Action.GLOW_CARDS
            action['client'] = client
            action['endAnimationFlag'] = False
            self.scenario.append(action)

        else:

            hero.destroyEptitudes()
            action = {}
            action['type'] = Action.SPELL_TARGET_WARNING
            action['client'] = client
            action['effect'] = False
            action['endAnimationFlag'] = False
            self.scenario.append(action)

    def spellToTargetForEffect (self, targetIndex, targetAttachment, whiteFlag):

        self.scenario = []

        if whiteFlag:
            cardData = self.white_hand[self.effectCardIndex]
            client = self.getWhiteId()

            hand = self.white_hand

            totalCardPrice = cardData['price'] + cardData['priceMixin']
            price = self.white_step_price - totalCardPrice

            hero = self.whiteHeroUnit

        else:
            cardData = self.black_hand[self.effectCardIndex]
            client = self.getBlackId()

            hand = self.black_hand

            totalCardPrice = cardData['price'] + cardData['priceMixin']
            price = self.black_step_price - totalCardPrice

            hero = self.blackHeroUnit

        self.spellTarget = self.getUnitByIndexAndAttachment(targetIndex, targetAttachment, whiteFlag)
        hero.configureEptitudes(self.effectCard)

        valid = self.validateSpellTarget (hero, whiteFlag)

        if valid:
            if self.spellTarget.spellInvisible:
                logger.debug('spellTarget is spellInvisible')
                valid = False

        if valid:
            del hand[self.effectCardIndex]
            if whiteFlag:
                self.white_step_price = price
            else:
                self.black_step_price = price

            action = {}
            action['type'] = Action.STEP_PRICE
            action['client'] = client
            action['price'] = price
            action['overload'] = self.stepOverload
            action['endAnimationFlag'] = False
            self.scenario.append (action)

            action = {}
            action['type'] = Action.DESTROY_ACTUAL_CARD
            action['enemy'] = True
            action['client'] = client
            action['cardIndex'] = self.effectCardIndex
            action['endAnimationFlag'] = False
            self.scenario.append(action)

            action = {}
            action['type'] = Action.SORT_DECK
            action['client'] = client
            action['endAnimationFlag'] = False
            self.scenario.append(action)

            logger.debug ('hand length: %s' % len(hand))

            logger.debug('card title: %s' % cardData['title'])

            self.controller = Controller()
            self.controller.setMatch(self)
            self.controller.setScenario(self.scenario)
            self.controller.setClient(client)
            self.controller.setWhiteFlag(whiteFlag)
            self.controller.spellToTarget(hero)

            hero.destroyEptitudes()

            if whiteFlag:
                row = self.whiteUnitRow
                opponentRow = self.blackUnitRow
            else:
                row = self.blackUnitRow
                opponentRow = self.whiteUnitRow

            for unit in row:
                self.controller.associateSpell(unit)
                self.controller.allSpell(unit)

            for unit in opponentRow:
                self.controller.opponentSpell(unit)
                self.controller.allSpell(unit)

            action = {}
            action['type'] = Action.UNBLOCK_DECK
            action['client'] = client
            action['endAnimationFlag'] = False
            self.scenario.append(action)

            if not self.seriesFlag:
                self.seriesFlag = True
                action = {}
                action['type'] = Action.ACTIVATE_DRAWING_SERIES
                action['client'] = client
                self.scenario.append(action)

            action = {}
            action['type'] = Action.GLOW_CARDS
            action['client'] = client
            action['endAnimationFlag'] = False
            self.scenario.append(action)

        else:

            hero.destroyEptitudes()
            action = {}
            action['type'] = Action.SPELL_TARGET_WARNING
            action['client'] = client
            action['effect'] = True
            action['endAnimationFlag'] = False
            self.scenario.append(action)



        #logger.debug ('price:%s' % price)


    def validateSpellTarget (self, unit, whiteFlag):
        valid = False
        validFlags = []
        for eptitude in unit.eptitudes:
            targets = self.getSpellTargets(eptitude, unit, whiteFlag)
            if eptitude.level == EptitudeLevel.SPELL_TARGET:
                try:
                    index = targets.index(self.spellTarget)
                    validFlags.append(True)
                except:
                    validFlags.append(False)
            else:
                validFlags.append(True)

        if len(validFlags) == 0:
            return valid

        valid = True
        for flag in validFlags:
            if flag == False:
                valid = False
        return valid

    def getSpellTargets (self, eptitude, unit, whiteFlag):
        targets = []
        if whiteFlag:
            hero = self.whiteHeroUnit
            opponentHero = self.blackHeroUnit
            row = self.whiteUnitRow
            opponentRow = self.blackUnitRow
        else:
            hero = self.blackHeroUnit
            opponentHero = self.whiteHeroUnit
            row = self.blackUnitRow
            opponentRow = self.whiteUnitRow

        try:
            raceId = eptitude.race
            Race.objects.get(id=raceId)
            raceFlag = True
        except:
            raceFlag = False

        if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
            for unit in row:
                 if raceFlag:
                    try:
                        if unit.race.id == raceId:
                            targets.append(unit)
                    except:
                         pass
                 else:
                     targets.append(unit)

            if eptitude.attachHero:
                targets.append(hero)

        elif eptitude.attachment == EptitudeAttachment.OPPONENT:
            for unit in opponentRow:
                if raceFlag:
                    try:
                        if unit.race.id == raceId:
                            targets.append(unit)
                    except:
                         pass
                else:
                     targets.append(unit)

            if eptitude.attachHero:
                targets.append(opponentHero)
        else:
            for unit in row:
                if raceFlag:
                    try:
                        if unit.race.id == raceId:
                            targets.append(unit)
                    except:
                         pass
                else:
                     targets.append(unit)
            if eptitude.attachHero:
                targets.append(hero)

            for unit in opponentRow:
                if raceFlag:
                    try:
                        if unit.race.id == raceId:
                            targets.append(unit)
                    except:
                         pass
                else:
                     targets.append(unit)
            if eptitude.attachHero:
                targets.append(opponentHero)

        # TODO getSpellCondition
        logger.debug ('eptitude.spellCondition:%s' % eptitude.spellCondition)
        if eptitude.spellCondition > 0:
            targets = self.filterCondition (eptitude, eptitude.spellCondition, targets, unit)

        return targets






    def addUnit(self, index, position, whiteFlag):
        self.scenario = []

        if whiteFlag:
            cardData = self.white_hand[index]
            del self.white_hand[index]
            unit = Unit(cardData)
            self.whiteUnitRow.insert (position, unit)
            unit.row = self.whiteUnitRow
            client = self.getWhiteId()
            totalCardPrice = cardData['price'] + cardData['priceMixin']
            price = self.white_step_price - totalCardPrice
            self.white_step_price = price
            rowLength = len (self.whiteUnitRow)
        else:
            cardData = self.black_hand[index]
            del self.black_hand[index]
            unit = Unit(cardData)
            self.blackUnitRow.insert (position, unit)
            unit.row = self.blackUnitRow
            client = self.getBlackId()
            totalCardPrice = cardData['price'] + cardData['priceMixin']
            price = self.black_step_price - totalCardPrice
            self.black_step_price = price
            rowLength = len (self.blackUnitRow)

        unit.setWhiteFlag (whiteFlag)

        list = []
        if whiteFlag:
            for item in self.whiteUnitRow:
                list.append (item.getTitle())
        else:
            for item in self.blackUnitRow:
                list.append (item.getTitle())

        #logger.debug ('row:%s' % list)


            # generateSelectedMask
            # checkMaskTargetsCount
            # if count == 0 continue classic scenario
            # else

        action = {}
        action['type'] = Action.STEP_PRICE
        action['client'] = client
        action['price'] = price
        action['overload'] = self.stepOverload
        action['endAnimationFlag'] = False
        self.scenario.append (action)



        '''
            Если у токена есть способность с уровнем применения SELECTED, то
            генерируем маску для селектед, помним о том, что мы уже исключили карту из руки и поставили токен на поле
            отправляем клиенту инициатору два отдельных сценария для выставления фишки на поле и для выбора цели
            если клиент выберет цель то в специальном сценарии просто отработаем способность по выбранной цели и информируем
            оппонента о выставлении фишки и срабатывании способности если выбор не сделан или пришло уведомление о неправильно
            выбранной цели, то возвращаем карту. Оппонента держим в неведнии о манипуляциях с полем фишек инциатора. На сервере
            мутим с рядами и картами инициатора

        '''

        if self.validateSelectedEptitudes (unit.eptitudes):

            mask = self.generateSelectedMask (whiteFlag, unit, position)

            # уточнаем способность
            selectedEptitude = self.getSelectedEptitude (unit.eptitudes)

            # проверяем есть ли в ней дополнительные условия
            # если есть фильтруем маску

            if selectedEptitude.getCondition() > 0:
                mask =  self.filterMaskCondition (whiteFlag, selectedEptitude.getCondition(), mask)

            if mask['count'] > 0:
                self.selected_unit = unit

                logger.debug ('initSelectedEptitudes')

                self.selectMode = True

                action = {}
                action['type'] = Action.DESTROY_ACTUAL_CARD
                action['client'] = client
                action['enemy'] = False
                action['cardIndex'] = index
                action['endAnimationFlag'] = False
                self.scenario.append(action)


                action = {}
                action['type'] = Action.SORT_DECK
                action['client'] = client
                action['endAnimationFlag'] = False
                self.scenario.append(action)

                action = {}
                action['type'] = Action.PLAY_CARD_SELECTED
                action['client'] = client
                action['unit'] = unit.getCardData()
                action['position'] = position
                action['endAnimationFlag'] = True
                action['cardIndex'] = index
                self.scenario.append(action)

                action = {}
                action['type'] = Action.PLAY_CARD_OPPONENT_SELECTED
                action['client'] = client
                action['unit'] = unit.getCardData()
                action['position'] = position
                action['endAnimationFlag'] = True
                action['cardIndex'] = index
                self.selected_action = action

                action = {}
                action['type'] = Action.SELECT
                action['client'] = client
                action['endAnimationFlag'] = False
                action['select_mask'] = mask
                self.scenario.append(action)
                return

            else:
               self.selectMask = False

        action = {}
        action['type'] = Action.PLAY_CARD_UNIT
        action['client'] = client
        action['unit'] = unit.getCardData()
        action['position'] = position
        action['endAnimationFlag'] = True
        action['cardIndex'] = index
        self.scenario.append(action)

        action = {}
        action['type'] = Action.SORT_DECK
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

        action = {}
        action['type'] = Action.SET_ROW_LENGTH
        action['client'] = client
        action['length'] = rowLength
        self.scenario.append (action)

        action = {}
        action['type'] = Action.UNBLOCK_DECK
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

        self.controller = Controller()
        self.controller.setMatch(self)
        self.controller.setScenario(self.scenario)
        self.controller.setClient(client)
        self.controller.setWhiteFlag(whiteFlag)
        self.controller.addUnit(unit)
        self.controller.unitPlaced (unit)

        self.controller = Controller()
        self.controller.setMatch(self)
        self.controller.setScenario(self.scenario)
        self.controller.setClient(client)
        self.controller.setWhiteFlag(whiteFlag)
        self.controller.playCard (unit)

        controller = CardController()
        controller.setWhiteFlag(whiteFlag)
        controller.setMatch(self)
        controller.setScenario(self.scenario)
        controller.setClient(client)
        controller.play_card()
        controller.new_unit()

        if not self.seriesFlag:
            self.seriesFlag = True
            action = {}
            action['type'] = Action.ACTIVATE_DRAWING_SERIES
            action['client'] = client
            self.scenario.append(action)

        action = {}
        action['type'] = Action.GLOW_CARDS
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)





    def continueAddUnit (self, selectData, whiteFlag):

        self.selectMask = selectData

        if whiteFlag:
            client = self.getWhiteId()
            rowLength = len (self.whiteUnitRow)
        else:
            client = self.getBlackId()
            rowLength = len (self.blackUnitRow)

        self.whiteFlag = whiteFlag

        self.scenario = []
        self.scenario.append (self.selected_action)

        self.controller = Controller()
        self.controller.setMatch(self)
        self.controller.setScenario(self.scenario)
        self.controller.setClient(client)
        self.controller.setWhiteFlag(whiteFlag)

        self.controller.addUnit(self.selected_unit)
        self.controller.unitPlaced (self.selected_unit)
        self.controller.playCard (self.selected_unit)

        action = {}
        action['type'] = Action.UNBLOCK_DECK
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

        if not self.seriesFlag:
            self.seriesFlag = True
            action = {}
            action['type'] = Action.ACTIVATE_DRAWING_SERIES
            action['client'] = client
            self.scenario.append(action)

        action = {}
        action['type'] = Action.GLOW_CARDS
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

        self.selectMode = False


        return self.scenario

    def cancelSelect (self, whiteFlag):

        cardData = self.selected_unit.cardData

        if whiteFlag:
            hand = self.white_hand
            row = self.whiteUnitRow
            opponentRow = self.blackUnitRow
            client = self.getWhiteId()
            totalCardPrice = cardData['price'] + cardData['priceMixin']
            price = self.white_step_price + totalCardPrice
            self.white_step_price = price
        else:
            hand = self.black_hand
            row = self.blackUnitRow
            client = self.getBlackId()
            totalCardPrice = cardData['price'] + cardData['priceMixin']
            price = self.black_step_price + totalCardPrice
            self.black_step_price = price
            opponentRow = self.whiteUnitRow

        cardData['price'] = cardData['defaultPrice']
        cardData['priceMixin'] = 0
        hand.append (cardData)

        selectAttachment = self.initAttachment (self.selected_unit, whiteFlag)
        selectIndex = self.initIndex (self.selected_unit, selectAttachment, whiteFlag)
        del row[selectIndex]

        scenario = []

        action = {}
        action['targetIndex'] = selectIndex
        action['targetAttachment'] = selectAttachment
        action['type'] = Action.BACK_TOKEN_TO_HAND
        action['client'] = client
        action['endAnimationFlag'] = True
        action['card'] = self.copyCard(cardData)
        scenario.append (action)

        self.lastCardinHand = cardData

        action = {}
        action['type'] = Action.STEP_PRICE
        action['client'] = client
        action['price'] = price
        action['overload'] = self.stepOverload
        action['endAnimationFlag'] = False
        scenario.append (action)

        action = {}
        action['type'] = Action.UNBLOCK_DECK
        action['client'] = client
        action['endAnimationFlag'] = False
        scenario.append(action)

        for unit in row:
            self.controller = Controller()
            self.controller.setMatch(self)
            self.controller.setScenario(scenario)
            self.controller.setClient(client)
            self.controller.setWhiteFlag(whiteFlag)
            self.controller.newCard(unit)
            self.controller.newPlayerCard(unit)



        action = {}
        action['type'] = Action.GLOW_CARDS
        action['client'] = client
        action['endAnimationFlag'] = False
        scenario.append(action)

        self.selectMode = False
        return scenario




    def getScenario (self):
        return self.scenario



    def classicAttack (self, initiatorIndex, targetIndex, whiteFlag):

        if whiteFlag:
            client = self.getWhiteId()
            attackUnit =  self.whiteUnitRow[initiatorIndex]
            if targetIndex >= 0:
                targetUnit = self.blackUnitRow[targetIndex]
            else:
                targetUnit = self.blackHeroUnit
        else:
            client = self.getBlackId()
            attackUnit = self.blackUnitRow[initiatorIndex]
            if targetIndex >= 0:
                targetUnit = self.whiteUnitRow[targetIndex]
            else:
                targetUnit = self.whiteHeroUnit

        self.scenario = []

        heroDeath = False


        # checkProvocation
        if self.notValidProvocation(whiteFlag, targetUnit):
             action = {}
             action['type'] = Action.PROVOCATION_EXCEPTION
             action['client'] = client
             action['endAnimationFlag'] = False
             self.scenario.append(action)
             return self.scenario

        #checkShadow
        if targetUnit.shadow:
            action = {}
            action['type'] = Action.SHADOW_EXCEPTION
            action['client'] = client
            action['endAnimationFlag'] = False
            self.scenario.append(action)
            return self.scenario

        self.targetUnit = targetUnit
        self.attackUnit = attackUnit

        controller = Controller()
        controller.setMatch(self)
        controller.setScenario(self.scenario)
        controller.setClient(client)
        controller.setWhiteFlag(whiteFlag)
        controller.preAttack(attackUnit)

        if attackUnit.whiteFlag:
            opponentRow = self.blackUnitRow
        else:
            opponentRow = self.whiteUnitRow

        for unit in opponentRow:
            controller = Controller()
            controller.setMatch(self)
            controller.setScenario(self.scenario)
            controller.setClient(client)
            controller.setWhiteFlag(whiteFlag)
            controller.opponentPreAttack(unit)

        targetUnit = self.targetUnit

        attackValue = attackUnit.getTotalAttack()
        targetAttackValue = attackValue
        targetHealthValue = targetUnit.getHealth()
        if targetUnit.shield and attackValue > 0:
            targetUnit.shield = False
            targetNewHealthValue = targetHealthValue
            action = {}
            action['type'] = Action.DESTROY_SHIELD
            action['client'] = client
            attachment = self.initAttachment (targetUnit, whiteFlag)
            index = self.initIndex (targetUnit, attachment, whiteFlag)
            action['index'] = index
            action['attachment'] = attachment
            action['endAnimationFlag'] = False
            targetShieldActionFlag = True
            targetShieldAction = action

            controller = CardController()
            controller.setWhiteFlag(whiteFlag)
            controller.setMatch(self)
            controller.setScenario(self.scenario)
            controller.setClient(client)
            controller.destroy_shield()
        else:
             targetShieldActionFlag = False
             targetNewHealthValue = targetHealthValue - attackValue
             targetUnit.setHealth(targetNewHealthValue)


        attackValue = targetUnit.getTotalAttack()
        initiatorAttackValue = attackValue
        initiatorHealthValue = attackUnit.getHealth()
        if attackUnit.shield and attackValue > 0:
            attackUnit.shield = False
            initiatorNewHealthValue = initiatorHealthValue
            action = {}
            action['type'] = Action.DESTROY_SHIELD
            action['client'] = client
            attachment = self.initAttachment (attackUnit, whiteFlag)
            index = self.initIndex (attackUnit, attachment, whiteFlag)
            action['index'] = index
            action['attachment'] = attachment
            action['endAnimationFlag'] = False
            initiatorShieldActionFlag = True
            initiatorShieldAction = action

            controller = CardController()
            controller.setWhiteFlag(whiteFlag)
            controller.setMatch(self)
            controller.setScenario(self.scenario)
            controller.setClient(client)
            controller.destroy_shield()
        else:
            initiatorShieldActionFlag = False
            initiatorNewHealthValue = initiatorHealthValue - attackValue
            attackUnit.setHealth(initiatorNewHealthValue)

        targetAttachment = self.initAttachment (targetUnit, whiteFlag)
        targetIndex = self.initIndex (targetUnit, targetAttachment, whiteFlag)

        initiatorAttachment = self.initAttachment(attackUnit, whiteFlag)

        action = {}
        action['type'] = Action.ATTACK
        action['client'] = client
        action['endAnimationFlag'] = True
        action['initiatorIndex'] = initiatorIndex
        action['targetIndex'] = targetIndex
        self.scenario.append(action)

        action = {}
        action['type'] = Action.ATTACK_COMPLETE
        action['client'] = client
        action['endAnimationFlag'] = True
        self.scenario.append(action)

        action = {}
        action['type'] = Action.DAMAGE
        action['client'] = client
        damageTargets = []
        action['targets'] = damageTargets

        if not targetShieldActionFlag:
             damageTargets.append({'index':targetIndex, 'attachment':targetAttachment, 'damage':targetAttackValue})

        if not initiatorShieldActionFlag and initiatorAttackValue > 0:
                damageTargets.append({'index':initiatorIndex, 'attachment':initiatorAttachment, 'damage':initiatorAttackValue})
        self.scenario.append(action)

        action = {}
        action['type'] = Action.HEALTH_AFTER_ATTACK
        action['client'] = client
        action['endAnimationFlag'] = False
        action['initiatorIndex'] = initiatorIndex
        action['targetIndex'] = targetIndex
        action["attackUnitHealth"] = attackUnit.getHealth()
        action["targetUnitHealth"] = targetUnit.getHealth()
        self.scenario.append(action)

        if targetShieldActionFlag:
            self.scenario.append (targetShieldAction)

        if initiatorShieldActionFlag:
            self.scenario.append (initiatorShieldAction)

        if targetNewHealthValue < targetHealthValue:
            if isinstance (targetUnit, Unit):
                self.controller = Controller()
                self.controller.setMatch(self)
                self.controller.setScenario(self.scenario)
                self.controller.setClient(client)
                self.controller.setWhiteFlag(whiteFlag)
                self.controller.woundUnit(targetUnit)

            if isinstance(targetUnit, HeroUnit):
                controller = CardController()
                controller.setWhiteFlag(whiteFlag)
                controller.setMatch(self)
                controller.setScenario(self.scenario)
                controller.setClient(client)
                controller.hero_wound(targetUnit.whiteFlag)



        if initiatorNewHealthValue < initiatorHealthValue:
            if isinstance (attackUnit, Unit):
                self.controller = Controller()
                self.controller.setMatch(self)
                self.controller.setScenario(self.scenario)
                self.controller.setClient(client)
                self.controller.setWhiteFlag(whiteFlag)
                self.controller.woundUnit(attackUnit)

        #logger.debug ('attackUnit.health:%s' % attackUnit.getHealth())
        self.lastAttackingUnit = attackUnit

        if isinstance(targetUnit, Unit):
            self.lastAttackedUnit = targetUnit

        self.lastAttacked = targetUnit

        controller = Controller()
        controller.setMatch(self)
        controller.setScenario(self.scenario)
        controller.setClient(client)
        controller.setWhiteFlag(whiteFlag)
        controller.attack(attackUnit)
        controller.isAttacked(targetUnit)



        if attackUnit.getHealth() <= 0:
                attackUnitDieFlag = True
                actionFlag = False

                if whiteFlag:
                    attackUnit.setIndex(initiatorIndex)
                    attackUnit.setRow(self.whiteUnitRow)
                    try:
                        self.whiteUnitRow.remove(attackUnit)
                        actionFlag = True
                    except:
                        pass

                else:
                    attackUnit.setIndex(initiatorIndex)
                    attackUnit.setRow(self.blackUnitRow)
                    try:
                        self.blackUnitRow.remove(attackUnit)
                        actionFlag = True
                    except:
                        pass

                if actionFlag:

                    #logger.debug ('addAction::attack_token_death')
                    action = {}
                    action['type'] = Action.ATTACK_TOKEN_DEATH
                    action['client'] = client
                    action['endAnimationFlag'] = True
                    action['initiatorIndex'] = initiatorIndex
                    self.scenario.append(action)

                    self.dieUnitsIndex += 1

                    self.controller = Controller()
                    self.controller.setMatch(self)
                    self.controller.setScenario(self.scenario)
                    self.controller.setClient(client)
                    self.controller.setWhiteFlag(whiteFlag)
                    self.controller.removeUnit(attackUnit)

                    controller = CardController()
                    controller.setWhiteFlag(whiteFlag)
                    controller.setMatch(self)
                    controller.setScenario(self.scenario)
                    controller.setClient(client)
                    controller.unit_die(targetUnit.whiteFlag)


        else:
            attackUnitDieFlag = False

        if targetUnit.getHealth() <=0:

                if targetIndex >= 0:

                    try:
                        if whiteFlag:
                             targetUnit.setIndex(targetIndex)
                             targetUnit.setRow(self.blackUnitRow)
                             self.blackUnitRow.remove(targetUnit)
                        else:
                             targetUnit.setIndex(targetIndex)
                             targetUnit.setRow(self.whiteUnitRow)
                             self.whiteUnitRow.remove(targetUnit)

                        aliveFlag = True
                    except:
                        aliveFlag = False

                    # уточняем живо ли существо или умерло еще до завершения классической аттаки в резултате срабатывания способности
                    if aliveFlag:
                        #logger.debug ('addAction::target_token_death')
                        action = {}
                        action['type'] = Action.TARGET_TOKEN_DEATH
                        action['client'] = client
                        action['endAnimationFlag'] = True
                        action['targetIndex'] = targetIndex
                        self.scenario.append(action)

                        self.dieUnitsIndex += 1

                        self.controller = Controller()
                        self.controller.setMatch(self)
                        self.controller.setScenario(self.scenario)
                        self.controller.setClient(client)
                        self.controller.setWhiteFlag(whiteFlag)
                        self.controller.removeUnit(targetUnit)

                        controller = CardController()
                        controller.setWhiteFlag(whiteFlag)
                        controller.setMatch(self)
                        controller.setScenario(self.scenario)
                        controller.setClient(client)
                        controller.unit_die(targetUnit.whiteFlag)
                else:
                    #logger.debug ('addAction::opponent_hero_death')
                    heroDeath = True



        if attackUnitDieFlag:
            pass
        else:
            if attackUnit.shadow:
                action = {}
                attackUnit.shadow = False
                action['type'] = Action.DESTROY_SHADOW
                action['client'] = client
                attachment = self.initAttachment (attackUnit, whiteFlag)
                index = self.initIndex (attackUnit, attachment, whiteFlag)
                action['index'] = index
                action['attachment'] = attachment
                action['endAnimationFlag'] = False
                self.scenario.append (action)

            stepAttack = attackUnit.stepAttack
            stepAttack = stepAttack - 1
            attackUnit.stepAttack = stepAttack
            logger.debug ('attackUnit.stepAttack: %s' % stepAttack)
            if stepAttack > 0:
                action = {}
                action['type'] = Action.ATTACK_AVAILABLE
                action['client'] = client
                action['endAnimationFlag'] = False
                da_units = []
                da_units.append (attackUnit.row.index(attackUnit))
                action['unitList'] = da_units
                self.scenario.append(action)

                action = {}
                action['type'] = Action.GLOW_UNITS
                action['client'] = client
                action['endAnimationFlag'] = False
                self.scenario.append(action)

        action = {}
        action['type'] = Action.GLOW_CARDS
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

        if heroDeath:

            self.endMatch(client, self.scenario, whiteFlag)



        '''
        list = []
        for item in self.whiteUnitRow:
            list.append (item.getTitle())

        list = []
        for item in self.blackUnitRow:
            list.append (item.getTitle())
        '''

        return self.scenario

    def setLastPlaced (self, unit):
        self.lastPlaced = unit

    def getCardsFromHand(self, unit, eptitude, attachment, whiteFlag):
        if attachment == EptitudeAttachment.ASSOCIATE:
            if whiteFlag:
                hand = self.white_hand
            else:
                hand = self.black_hand
        elif attachment == EptitudeAttachment.OPPONENT:
            if whiteFlag:
                hand = self.black_hand
            else:
                hand = self.white_hand
        targets = []
        for card in hand:
            targets.append(card)

        self.filterCondition(eptitude,eptitude.condition,targets, unit)


    def getLevelTargets (self, unit, eptitude, whiteFlag):

        if whiteFlag:
           row = self.whiteUnitRow
           opponentRow = self.blackUnitRow
           hero = self.whiteHeroUnit
           opponentHero = self.blackHeroUnit
        else:
           row = self.blackUnitRow
           opponentRow = self.whiteUnitRow
           hero = self.blackHeroUnit
           opponentHero = self.whiteHeroUnit

        levelList = []
        if eptitude.level == EptitudeLevel.SELF:
            levelList.append(unit)

        if eptitude.level == EptitudeLevel.NEIGHBORS:
            if unit.whiteFlag:
                row = self.whiteUnitRow
            else:
                row = self.blackUnitRow

            index = row.index (unit)
            leftNeighborIndex = index - 1
            if leftNeighborIndex >= 0:
                leftNeighbor = row[leftNeighborIndex]
                levelList.append(leftNeighbor)

            try:
                rightNeightbor = row[index + 1]
                levelList.append(rightNeightbor)
            except:
                pass


        if eptitude.level == EptitudeLevel.SELECTED:
            try:
                index = self.selectMask['index']
                if self.selectMask['player']:
                     if index < 0:
                         levelList.append(hero)
                     else:
                         levelList.append(row[index])
                else:
                     if index < 0:
                         levelList.append(opponentHero)
                     else:
                         levelList.append(opponentRow[index])
            except:
                pass


        if eptitude.level == EptitudeLevel.RANDOM:

            if unit.whiteFlag:
                row = self.whiteUnitRow
                opponentRow = self.blackUnitRow
                hero = self.whiteHeroUnit
                opponentHero = self.blackHeroUnit
            else:
                row = self.blackUnitRow
                opponentRow = self.whiteUnitRow
                hero = self.blackHeroUnit
                opponentHero = self.whiteHeroUnit

            try:
                raceId = eptitude.race
                Race.objects.get(id=raceId)
                raceFlag = True
            except:
                raceFlag = False


            if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
                for item in row:
                    if item != unit:
                        if raceFlag:
                            try:
                                if item.race.id == raceId:
                                    levelList.append(item)
                            except:
                                pass
                        else:
                             levelList.append(item)
                    else:
                        if eptitude.attachInitiator:
                            if raceFlag:
                                try:
                                    if item.race.id == raceId:
                                        levelList.append(item)
                                except:
                                    pass
                            else:
                                levelList.append(item)

                if eptitude.attachHero:
                    levelList.append (hero)

            elif eptitude.attachment == EptitudeAttachment.OPPONENT:
                for item in opponentRow:
                    if raceFlag:
                        try:
                            if item.race.id == raceId:
                                levelList.append(item)
                        except:
                            pass
                    else:
                        levelList.append(item)

                if eptitude.attachHero:
                    levelList.append (opponentHero)
            else:
               for item in row:
                    if item != unit:
                        if raceFlag:
                            try:
                                if item.race.id == raceId:
                                    levelList.append(item)
                            except:
                                pass
                        else:
                             levelList.append(item)
                    else:
                        if eptitude.attachInitiator:
                            if raceFlag:
                                try:
                                    if item.race.id == raceId:
                                        levelList.append(item)
                                except:
                                    pass
                            else:
                                levelList.append(item)

               if eptitude.attachHero:
                    levelList.append (hero)


               for item in opponentRow:
                    if raceFlag:
                        if item.race.id == raceId:
                            levelList.append(item)
                    else:
                        levelList.append(item)

               if eptitude.attachHero:
                    levelList.append (opponentHero)

            if eptitude.getCondition() > 0:
                levelList = self.filterCondition (eptitude, eptitude.getCondition(), levelList, unit)

            levelList = self.initRandom (levelList)

        if eptitude.level == EptitudeLevel.All:

            if unit.whiteFlag:
                row = self.whiteUnitRow
                opponentRow = self.blackUnitRow
                hero = self.whiteHeroUnit
                opponentHero = self.blackHeroUnit
            else:
                row = self.blackUnitRow
                opponentRow = self.whiteUnitRow
                hero = self.blackHeroUnit
                opponentHero = self.whiteHeroUnit

            try:
                raceId = eptitude.race
                Race.objects.get(id=raceId)
                raceFlag = True
            except:
                raceFlag = False

            if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
                for item in row:
                    if item != unit:
                        if raceFlag:
                            try:
                                if item.race.id == raceId:
                                    levelList.append(item)
                            except:
                                pass
                        else:
                             levelList.append(item)
                    else:
                        if eptitude.attachInitiator:
                            if raceFlag:
                                try:
                                    if item.race.id == raceId:
                                        levelList.append(item)
                                except:
                                    pass
                            else:
                                levelList.append(item)

                if eptitude.attachHero:
                    levelList.append (hero)

            elif eptitude.attachment == EptitudeAttachment.OPPONENT:
                for item in opponentRow:
                    if raceFlag:
                        try:
                            if item.race.id == raceId:
                                levelList.append(item)
                        except:
                            pass
                    else:
                        levelList.append(item)

                if eptitude.attachHero:
                    levelList.append (opponentHero)
            else:
               for item in row:
                    if item != unit:
                        if raceFlag:
                            try:
                                if item.race.id == raceId:
                                    levelList.append(item)
                            except:
                                pass
                        else:
                             levelList.append(item)
                    else:
                        if eptitude.attachInitiator:
                            if raceFlag:
                                try:
                                    if item.race.id == raceId:
                                        levelList.append(item)
                                except:
                                    pass
                            else:
                                levelList.append(item)

               if eptitude.attachHero:
                    levelList.append (hero)


               for item in opponentRow:
                    if raceFlag:
                        if item.race.id == raceId:
                            levelList.append(item)
                    else:
                        levelList.append(item)

               if eptitude.attachHero:
                    levelList.append (opponentHero)


        if eptitude.level == EptitudeLevel.ALL_EXCEPT_ONE:
            if unit.whiteFlag:
                row = self.whiteUnitRow
                opponentRow = self.blackUnitRow
                hero = self.whiteHeroUnit
                opponentHero = self.blackHeroUnit
            else:
                row = self.blackUnitRow
                opponentRow = self.whiteUnitRow
                hero = self.blackHeroUnit
                opponentHero = self.whiteHeroUnit

            try:
                raceId = eptitude.race
                Race.objects.get(id=raceId)
                raceFlag = True
            except:
                raceFlag = False

            if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
                for item in row:
                    if item != unit:
                        if raceFlag:
                            try:
                                if item.race.id == raceId:
                                    levelList.append(item)
                            except:
                                pass
                        else:
                             levelList.append(item)
                    else:
                        if eptitude.attachInitiator:
                            if raceFlag:
                                try:
                                    if item.race.id == raceId:
                                        levelList.append(item)
                                except:
                                    pass
                            else:
                                levelList.append(item)

                if eptitude.attachHero:
                    levelList.append (hero)

            elif eptitude.attachment == EptitudeAttachment.OPPONENT:
                for item in opponentRow:
                    if raceFlag:
                        try:
                            if item.race.id == raceId:
                                levelList.append(item)
                        except:
                            pass
                    else:
                        levelList.append(item)

                if eptitude.attachHero:
                    levelList.append (opponentHero)
            else:
               for item in row:
                    if item != unit:
                        if raceFlag:
                            try:
                                if item.race.id == raceId:
                                    levelList.append(item)
                            except:
                                pass
                        else:
                             levelList.append(item)
                    else:
                        if eptitude.attachInitiator:
                            if raceFlag:
                                try:
                                    if item.race.id == raceId:
                                        levelList.append(item)
                                except:
                                    pass
                            else:
                                levelList.append(item)

               if eptitude.attachHero:
                    levelList.append (hero)


               for item in opponentRow:
                    if raceFlag:
                        if item.race.id == raceId:
                            levelList.append(item)
                    else:
                        levelList.append(item)

               if eptitude.attachHero:
                    levelList.append (opponentHero)

               index = random.randint(0, len(levelList) - 1)
               del levelList[index]



        if eptitude.level == EptitudeLevel.UNIT_HERO:
            if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
                if unit.whiteFlag:
                    levelList.append(self.whiteHeroUnit)
                else:
                    levelList.append(self.blackHeroUnit)
            if eptitude.attachment == EptitudeAttachment.OPPONENT:
                if unit.whiteFlag:
                    levelList.append(self.blackHeroUnit)
                else:
                    levelList.append(self.whiteHeroUnit)
            if eptitude.attachment == EptitudeAttachment.ALL:
                levelList.append (self.whiteHeroUnit)
                levelList.append (self.blackHeroUnit)

        if eptitude.level == EptitudeLevel.HERO:
            if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
                if whiteFlag:
                    levelList.append(self.whiteHeroUnit)
                else:
                    levelList.append(self.blackHeroUnit)
            if eptitude.attachment == EptitudeAttachment.OPPONENT:
                if whiteFlag:
                    levelList.append(self.blackHeroUnit)
                else:
                    levelList.append(self.whiteHeroUnit)
            if eptitude.attachment == EptitudeAttachment.ALL:
                levelList.append (self.whiteHeroUnit)
                levelList.append (self.blackHeroUnit)


        if eptitude.level == EptitudeLevel.LAST_PLACED:
            try:
                raceId = eptitude.race
                Race.objects.get(id=raceId)
                raceFlag = True
            except:
                raceFlag = False

            if raceFlag:
                try:
                    if self.lastPlaced.race.id == raceId:
                        levelList.append(self.lastPlaced)
                except:
                    pass
            else:
                levelList.append(self.lastPlaced)

        if eptitude.level == EptitudeLevel.ALL_CARDS_IN_HAND:

            if unit.whiteFlag:
               playerHand = self.white_hand
               opponentHand = self.black_hand
            else:
               playerHand = self.black_hand
               opponentHand = self.white_hand

            try:
                raceId = eptitude.race
                Race.objects.get(id=raceId)
                raceFlag = True
            except:
                raceFlag = False

            if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
                for card in playerHand:
                    if raceFlag:
                        try:
                            if card['raceId'] == raceId:
                                levelList.append(card)
                        except:
                            pass
                    else:
                        levelList.append(card)


            elif eptitude.attachment == EptitudeAttachment.OPPONENT:
                for card in opponentHand:
                    if raceFlag:
                        try:
                            if card['raceId'] == raceId:
                                levelList.append(card)
                        except:
                            pass
                    else:
                        levelList.append(card)

            else:
                for card in playerHand:
                    if raceFlag:
                        try:
                            if card['raceId'] == raceId:
                                levelList.append(card)
                        except:
                            pass
                    else:
                        levelList.append(card)

                for card in opponentHand:
                    if raceFlag:
                        try:
                            if card['raceId'] == raceId:
                                levelList.append(card)
                        except:
                            pass
                    else:
                        levelList.append(card)

        if eptitude.level == EptitudeLevel.RANDOM_CARD_IN_HAND:

            if unit.whiteFlag:
               playerHand = self.white_hand
               opponentHand = self.black_hand
            else:
               playerHand = self.black_hand
               opponentHand = self.white_hand

            try:
                raceId = eptitude.race
                Race.objects.get(id=raceId)
                raceFlag = True
            except:
                raceFlag = False

            if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
                for card in playerHand:
                    if raceFlag:
                        try:
                            if card['raceId'] == raceId:
                                levelList.append(card)
                        except:
                            pass
                    else:
                        levelList.append(card)


            elif eptitude.attachment == EptitudeAttachment.OPPONENT:
                for card in opponentHand:
                    if raceFlag:
                        try:
                            if card['raceId'] == raceId:
                                levelList.append(card)
                        except:
                            pass
                    else:
                        levelList.append(card)

            else:
                for card in playerHand:
                    if raceFlag:
                        try:
                            if card['raceId'] == raceId:
                                levelList.append(card)
                        except:
                            pass
                    else:
                        levelList.append(card)

                for card in opponentHand:
                    if raceFlag:
                        try:
                            if card['raceId'] == raceId:
                                levelList.append(card)
                        except:
                            pass
                    else:
                        levelList.append(card)

            levelList = self.initRandom (levelList)

        if eptitude.level == EptitudeLevel.LAST_CARD_IN_HAND:
            try:
                raceId = eptitude.race
                Race.objects.get(id=raceId)
                raceFlag = True
            except:
                raceFlag = False

            card = self.lastCardinHand
            if raceFlag:
                try:
                    if card['raceId'] == raceId:
                        levelList.append(card)
                except:
                    pass
            else:
                levelList.append(card)

        if eptitude.level == EptitudeLevel.LAST_PLAYER_CARD_IN_HAND:
            try:
                raceId = eptitude.race
                Race.objects.get(id=raceId)
                raceFlag = True
            except:
                raceFlag = False

            card = self.getPlayerLastCard(unit.whiteFlag)
            if raceFlag:
                try:
                    if card['raceId'] == raceId:
                        levelList.append(card)
                except:
                    pass
            else:
                levelList.append(card)

        if eptitude.level == EptitudeLevel.LAST_OPPONENT_CARD_IN_HAND:
            try:
                raceId = eptitude.race
                Race.objects.get(id=raceId)
                raceFlag = True
            except:
                raceFlag = False

            card = self.getOpponentLastCard(unit.whiteFlag)
            if raceFlag:
                try:
                    if card['raceId'] == raceId:
                        levelList.append(card)
                except:
                    pass
            else:
                levelList.append(card)

        if eptitude.level == EptitudeLevel.LAST_ATTACKED:
            if isinstance (self.lastAttacked, Unit):
                if unit.whiteFlag:
                    row = self.whiteUnitRow
                    opponentRow = self.blackUnitRow
                else:
                    row = self.blackUnitRow
                    opponentRow = self.whiteUnitRow

                aliveFlag = False
                try:
                    row.index(self.lastAttacked)
                    aliveFlag = True
                except:
                    pass

                try:
                    opponentRow.index(self.lastAttacked)
                    aliveFlag = True
                except:
                    pass

                if aliveFlag:
                    levelList.append(self.lastAttacked)
            else:
                levelList.append(self.lastAttacked)

        if eptitude.level == EptitudeLevel.LAST_ATTACKED_UNIT:
            if unit.whiteFlag:
                row = self.whiteUnitRow
                opponentRow = self.blackUnitRow
            else:
                row = self.blackUnitRow
                opponentRow = self.whiteUnitRow


            aliveFlag = False
            try:
                row.index(self.lastAttackedUnit)
                aliveFlag = True
            except:
                pass

            try:
                opponentRow.index(self.lastAttackedUnit)
                aliveFlag = True
            except:
                pass

            try:
                raceId = eptitude.race
                Race.objects.get(id=raceId)
                raceFlag = True
            except:
                raceFlag = False

            if aliveFlag:
                  if raceFlag:
                      try:
                           if self.lastAttackedUnit.race.id == raceId:
                                levelList.append(self.lastAttackedUnit)
                      except:
                            pass
                  else:
                         levelList.append(self.lastAttackedUnit)



        if eptitude.level == EptitudeLevel.LAST_ATTACKING_UNIT:
            try:
                raceId = eptitude.race
                Race.objects.get(id=raceId)
                raceFlag = True
            except:
                raceFlag = False

            if raceFlag:
                  try:
                       if self.lastAttackingUnit.race.id == raceId:
                            levelList.append(self.lastAttackingUnit)
                  except:
                        pass
            else:
                  levelList.append(self.lastAttackingUnit)

        if eptitude.level == EptitudeLevel.ACTIVE_PLAYER:
            if whiteFlag:
                levelList.append(self.whiteHeroUnit)
            else:
                levelList.append(self.blackHeroUnit)

        if eptitude.level == EptitudeLevel.SPELL_TARGET:
            levelList.append(self.spellTarget)

        if eptitude.level == EptitudeLevel.SPELL_TARGET_ALLIES:
            if self.spellTarget.whiteFlag:
                row = self.whiteUnitRow
                hero = self.whiteHeroUnit
            else:
                row = self.blackUnitRow
                hero = self.blackHeroUnit

            if isinstance(self.spellTarget, HeroUnit):
                for unit in row:
                    levelList.append(unit)
            else:
                if eptitude.attachHero:
                    levelList.append(hero)
                for unit in row:
                    if unit != self.spellTarget:
                        levelList.append(unit)

        if eptitude.level == EptitudeLevel.SPELL_TARGET_NEIGHBORS:
            dieFlag = False
            try:
                 index = self.whiteUnitRow.index(self.spellTarget)
                 row = self.whiteUnitRow
            except:
                try:
                    index = self.blackUnitRow.index(self.spellTarget)
                    row = self.blackUnitRow
                except:
                    row = self.spellTarget.row
                    index = self.spellTarget.index
                    dieFlag = True


            try:
                leftNeighborIndex = index - 1
                if leftNeighborIndex >= 0:
                    leftNeighbor = row[leftNeighborIndex]
                    levelList.append(leftNeighbor)
            except:
                pass

            try:
                if dieFlag:
                    rightNeightbor = row[index]
                    levelList.append(rightNeightbor)
                else:
                    rightNeightbor = row[index + 1]
                    levelList.append(rightNeightbor)
            except:
                pass





        if eptitude.getCondition() > 0:
            levelList = self.filterCondition (eptitude, eptitude.getCondition(), levelList, unit)

        return levelList

    def initRandom (self, levellist):
        finalList = []
        if len(levellist):
            try:
                index = random.randint(0, len(levellist) - 1)
                finalList.append (levellist[index])
            except:
                finalList.append[levellist[0]]

        return finalList



    def filterCondition (self, eptitude, condition, levelList, unit):
        finalList = []
        logger.debug ('filterCondition: %s' % condition)
        for item in levelList:
            if condition == EptitudeCondition.HAS_SELF_DIE_EPTITUDE:
                if item.hasEptitudeWithPeriod(EptitudePeriod.SELF_DIE):
                   finalList.append(item)

            if condition == EptitudeCondition.LAST_PLACED_HAS_SELF_DIE_EPTITUDE:
                if self.lastPlaced.hasEptitudeWithPeriod(EptitudePeriod.SELF_DIE):
                   finalList.append(item)

            if condition == EptitudeCondition.ATTACK_MORE_THAN_6:
                if item.getTotalAttack() > 6:
                    finalList.append(item)

            if condition == EptitudeCondition.ATTACK_MORE_THAN_4:
                if item.getTotalAttack() > 4:
                    finalList.append(item)

            if condition == EptitudeCondition.ATTACK_LESS_THAN_3:
                if item.getTotalAttack() < 3:
                    finalList.append(item)

            if condition == EptitudeCondition.ATTACK_LESS_THAN_4:
                if item.getTotalAttack() < 4:
                    finalList.append(item)

            if condition == EptitudeCondition.HAS_BATTLECRY_EPTITUDE:
                addFlag = False
                for eptitute in item['eptitudes']:
                    if eptitute['battlecry'] == True:
                        addFlag = True

                if addFlag:
                    finalList.append(item)

            if condition == EptitudeCondition.ASSOCIATE_CONTROL_MEHANIZM_UNITS:
                controlFlag = False
                if item.whiteFlag:
                    row = self.whiteUnitRow
                else:
                    row = self.blackUnitRow
                for unit in row:
                    if unit.race.id == 7:
                        controlFlag = True

                if controlFlag:
                    finalList.append(item)

            if condition == EptitudeCondition.ASSOCIATE_NO_CONTROL_MEHANIZM_UNITS:
                controlFlag = False
                if item.whiteFlag:
                    row = self.whiteUnitRow
                else:
                    row = self.blackUnitRow
                for unit in row:
                    if unit.race.id == 7:
                        controlFlag = True

                if not controlFlag:
                    finalList.append(item)

            if condition == EptitudeCondition.OPPONENT_ROW_LENGTH_MORE_THAN_3:
                if unit.whiteFlag:
                    row = self.blackUnitRow
                else:
                    row = self.whiteUnitRow
                if len(row) > 3:
                    finalList.append(item)

            if condition == EptitudeCondition.ATTACK_EQUALS_TO_1:
                if item.attack == 1:
                    finalList.append(item)

            if condition == EptitudeCondition.FULL_HEALTH:
                if item.getHealth() == item.maxHealth:
                    finalList.append(item)

            if condition == EptitudeCondition.NOT_FULL_HEALTH:
                if item.getHealth() < item.maxHealth:
                    finalList.append(item)

            if condition == EptitudeCondition.FREEZE:
                if item.freeze:
                    finalList.append(item)

            if condition == EptitudeCondition.SPELL_TARGET_DEAD:
                spellTargetFlag = False
                try:
                    index = self.whiteUnitRow.index(self.spellTarget)
                    spellTargetFlag = True
                except:
                    pass
                try:
                    index = self.blackUnitRow.index(self.spellTarget)
                    spellTargetFlag = True
                except:
                    pass
                if not spellTargetFlag:
                    finalList.append(item)

            if condition == EptitudeCondition.SPELL_TARGET_NOT_FULL_HEALTH:
                if self.spellTarget.getHealth() < self.spellTarget.maxHealth:
                    finalList.append(item)

            if condition == EptitudeCondition.NOT_DRAWING_SERIES:
                if not self.seriesFlag:
                    finalList.append(item)

            if condition == EptitudeCondition.DRAWING_SERIES:
                if self.seriesFlag:
                    finalList.append(item)

            if condition == EptitudeCondition.ATTACHED_EPTITUDE:
                if eptitude.attached:
                    finalList.append(item)

            if condition == EptitudeCondition.ANIMAL_CARD:
                try:
                    logger.debug ('raceId:%s' % item['raceId'])
                    if item['raceId'] == 3:
                        finalList.append(item)
                except:
                    pass

            if condition == EptitudeCondition.UNIT_IN_SHADOW:
                if item.shadow == True:
                    finalList.append(item)

            if condition == EptitudeCondition.FULL_MANA:
                if unit.whiteFlag:
                    if self.white_price >= 10:
                         finalList.append(item)
                else:
                    if self.black_price >= 10:
                        finalList.append(item)

            if condition == EptitudeCondition.DEMON_UNIT:
                try:
                    if item.race.id == 2:
                        finalList.append(item)
                except:
                    pass

            if condition == EptitudeCondition.NOT_DEMON_UNIT:
                try:

                    if item.race.id != 2:
                        finalList.append(item)
                except:
                    finalList.append(item)





                    #if unit.race

        return finalList

    def filterMaskCondition (self, whiteFlag, condition, mask):
       associate = []
       opponent = []
       mask['count'] = 0

       if whiteFlag:
           playerRow = self.whiteUnitRow
           opponentRow = self.blackUnitRow
       else:
           playerRow = self.blackUnitRow
           opponentRow = self.whiteUnitRow

       for index in mask['associate']:
           unit = playerRow[index]

           if condition == EptitudeCondition.ATTACK_MORE_THAN_6:
               if unit.getTotalAttack() > 6:
                    associate.append (index)
                    mask['count'] += 1

       for index in mask['opponent']:
           unit = opponentRow[index]

           if condition == EptitudeCondition.ATTACK_MORE_THAN_6:
               if unit.getTotalAttack() > 6:
                    opponent.append (index)
                    mask['count'] += 1

       mask['associate'] = associate
       mask['opponent'] = opponent

       if mask['player_hero']:
           mask['count'] += 1

       if mask['opponent_hero']:
           mask['count'] += 1

       return mask





    def getTargetsIndexes(self, targets, whiteFlag):
        indexes = list()
        # токены клиента
        indexes.append(list())
        # токены противника
        indexes.append(list())

        # герой клиента
        # indexes[2]
        indexes.append(False)

        # герой противника
        # indexes[3]
        indexes.append(False)

        for target in targets:
            try:
                index = self.whiteUnitRow.index(target)
                indexes[0].append (index)
            except:
                pass

            try:
                index = self.blackUnitRow.index(target)
                indexes[1].append (index)
            except:
                pass

            if target == self.whiteHeroUnit:
                indexes[3] = True

            if target == self.blackHeroUnit:
                indexes[4] = True



        return indexes

    def notValidProvocation(self, whiteFlag, targetUnit):
        if whiteFlag:
            opponentRow = self.blackUnitRow
        else:
            opponentRow = self.whiteUnitRow

        if self.opponentRowContainsProvocators (opponentRow):
            if targetUnit.isProvocator():
               return False
            else:
                return True
        else:
            return False

    def opponentRowContainsProvocators (self, row):
        flag = False
        for item in row:
            if item.isProvocator() and item.shadow == False:
                flag = True
        return flag

    def validateSelectedEptitudes (self, eptitudes):
        selectedFlag = False
        for eptitude in eptitudes:
            if eptitude.level == EptitudeLevel.SELECTED:
                selectedFlag = True
        return selectedFlag

    def getSelectedEptitude (self, eptitudes):
        selectedEptitude = False
        for eptitude in eptitudes:
            if eptitude.level == EptitudeLevel.SELECTED:
                selectedEptitude = eptitude
        return selectedEptitude

    def generateSelectedMask (self, whiteFlag, unit, position):

        mask = {}
        mask['associate'] = []
        mask['opponent'] = []
        mask['player_hero'] = False
        mask['opponent_hero'] = False
        mask['count'] = 0

        if whiteFlag:
            row = self.whiteUnitRow
            opponentRow = self.blackUnitRow

        else:
            row = self.blackUnitRow
            opponentRow = self.whiteUnitRow

        for eptitude in unit.eptitudes:
            if eptitude.level == EptitudeLevel.SELECTED:
                maskEptitude = eptitude

        if maskEptitude.attachment == EptitudeAttachment.ASSOCIATE:
            for rowUnit in row:
                if rowUnit != unit:
                    mask['associate'].append(row.index(rowUnit))
                    count = mask['count']
                    mask['count'] = count + 1
                else:
                    if maskEptitude.attachInitiator:
                        mask['associate'].append(row.index(rowUnit))
                        count = mask['count']
                        mask['count'] = count + 1

            if maskEptitude.attachHero:
                mask['player_hero'] = True
                count = mask['count']
                mask['count'] = count + 1

        if maskEptitude.attachment == EptitudeAttachment.OPPONENT:
            for rowUnit in opponentRow:
                if rowUnit.shadow:
                    pass
                else:
                    mask['opponent'].append (opponentRow.index(rowUnit))
                    count = mask['count']
                    mask['count'] = count + 1

            if eptitude.attachHero:
                mask['opponent_hero'] = True
                count = mask['count']
                mask['count'] = count + 1

        if maskEptitude.attachment == EptitudeAttachment.ALL:
            for rowUnit in row:
                if rowUnit != unit:
                    mask['associate'].append(row.index(rowUnit))
                    count = mask['count']
                    mask['count'] = count + 1
                else:
                    if maskEptitude.attachInitiator:
                        mask['associate'].append(row.index(rowUnit))
                        count = mask['count']
                        mask['count'] = count + 1

            for rowUnit in opponentRow:
               if rowUnit.shadow:
                    pass
               else:
                    mask['opponent'].append (opponentRow.index(rowUnit))
                    count = mask['count']
                    mask['count'] = count + 1


            if maskEptitude.attachHero:
                mask['player_hero'] = True
                mask['opponent_hero'] = True
                count = mask['count']
                mask['count'] = count + 2

        return mask

    def initAttachment (self, unit, whiteFlag):
        attachment = - 1
        if unit == self.whiteHeroUnit:
            if whiteFlag:
                attachment = 1
            else:
                attachment = 0

        if unit == self.blackHeroUnit:
            if whiteFlag:
                attachment = 0
            else:
                attachment = 1

        try:
            self.whiteUnitRow.index(unit)
            if whiteFlag:
                attachment = 1
            else:
                attachment = 0
        except ValueError:
            pass

        try:
            self.blackUnitRow.index(unit)
            if whiteFlag:
                attachment = 0
            else:
                attachment = 1
        except ValueError:
            pass

        return attachment



    def initIndex (self, unit, attachment, whiteFlag):
        if attachment:
            if whiteFlag:
                row = self.whiteUnitRow
            else:
                row = self.blackUnitRow
        else:
            if whiteFlag:
                row = self.blackUnitRow
            else:
                row = self.whiteUnitRow

        try:
            index = row.index(unit)
            return index
        except ValueError:
            return - 1

    def initCardAttachment (self, card, whiteFlag):
        if card['whiteFlag'] == whiteFlag:
            attachment = 1
        else:
            attachment = 0

        try:
            index = self.white_hand.index(card)
        except:
            try:
                index = self.black_hand.index(card)
            except:
                index = -1

        return attachment, index

    def getUnitByIndexAndAttachment (self, targetIndex, targetAttachment, whiteFlag):

         if whiteFlag:
            if targetAttachment:
                if targetIndex >= 0:
                    target = self.blackUnitRow[targetIndex]
                else:
                    target = self.blackHeroUnit
            else:
                 if targetIndex >= 0:
                    target = self.whiteUnitRow[targetIndex]
                 else:
                    target = self.whiteHeroUnit
         else:
            if targetAttachment:
                 if targetIndex >= 0:
                    target = self.whiteUnitRow[targetIndex]
                 else:
                    target = self.whiteHeroUnit
            else:
                if targetIndex >= 0:
                    target = self.blackUnitRow[targetIndex]
                else:
                    target = self.blackHeroUnit

         return target































