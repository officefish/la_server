__author__ = 'inozemcev'

from card.models import Deck, Card
from hero.models import UserHero
from random import shuffle
import json
import math

from game.logic.controller import Controller, EptitudeLevel, EptitudeAttachment
from game.logic.action import Action
from game.logic.unit import Unit, HeroUnit, UnitEptitude


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
        self.blackHeroUnit = HeroUnit(self.blackHealth)

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
                cardData = self.getUnitCardData(card)
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
                cardData = self.getUnitCardData(card)
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

    def getUnitCardData (self, card):
        cardData = dict()
        cardData['title'] = card.title
        cardData['description'] = card.description
        cardData['price'] = card.price
        cardData['health'] = card.health
        cardData['attack'] = card.attack
        cardData['id'] = card.id
        cardData['type'] = card.type
        try:
            cardData['race'] = card.race.title
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
        eptitudeData['lifecycle'] = eptitude.lifecycle
        eptitudeData['attachment'] = eptitude.attachment
        eptitudeData['attach_hero'] = eptitude.attach_hero
        eptitudeData['attach_initiator'] = eptitude.attach_initiator
        try:
            eptitudeData['race'] = eptitude.race.id
        except: pass
        try:
            eptitudeData['subrace'] = eptitude.subrace.id
        except: pass
        try:
            eptitudeData['unit'] = eptitude.unit.id
        except: pass
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

    def getCard(self, whiteFlag):
        if whiteFlag:
             self.play_card = self.white_match_deck[:1][0]
             self.white_match_deck[:1] = []
             self.white_hand.append(self.play_card)
        else:
             self.play_card = self.black_match_deck[:1][0]
             self.black_match_deck[:1] = []
             self.black_hand.append(self.play_card)

        logger.debug(self.play_card)
        return self.play_card

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
            del row[index]
        else:
            del opponentRow[index]

    def start(self):

        self.incrementPrice(True)
        self.initStepPrice ()
        self.transitionProgress ()

        card = self.getCard(True)
        client = self.getWhiteId()
        price = self.getStepPrice(True)

        self.scenario = []

        action = {}
        action['type'] = Action.STEP_PRICE
        action['client'] = client
        action['price'] = price
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
        action['attachment'] = 1
        action['card'] = card
        action['endAnimationFlag'] = True
        self.scenario.append(action)

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

        #self.runStepTimer()
        return self.scenario

    def endStep (self):

        self.scenario = []
        self.transitionProgress ()

        whiteFlag = self.getStepFlag()

        self.incrementPrice(whiteFlag)
        self.initStepPrice ()

        card = self.getCard(whiteFlag)
        price = self.getStepPrice(whiteFlag)

        if whiteFlag:
            row = self.whiteUnitRow
            client = self.getWhiteId()
        else:
            row = self.blackUnitRow
            client = self.getBlackId()

        action = {}
        action['type'] = Action.STOP_STEP_TIMER
        self.scenario.append (action)

        action = {}
        action['type'] = Action.STEP_PRICE
        action['client'] = client
        action['price'] = price
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
        action['attachment'] = 1
        action['card'] = card
        action['endAnimationFlag'] = True
        self.scenario.append(action)

        action = {}
        action['type'] = Action.STEP
        action['client'] = client
        self.scenario.append(action)

        action = {}
        action['type'] = Action.UNBLOCK_DECK
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

        if len(row) < 7:
            action = {}
            action['type'] = Action.GLOW_CARDS
            action['client'] = client
            action['endAnimationFlag'] = False
            self.scenario.append(action)

        action = {}
        action['type'] = Action.ATTACK_AVAILABLE
        action['client'] = client
        action['endAnimationFlag'] = False
        units = []
        for unit in row:
            if unit.canAttack and unit.attack > 0:
                unit.setStepAttack (unit.attack)
                units.append (row.index(unit))

        action['unitList'] = units
        self.scenario.append(action)

        action = {}
        action['type'] = Action.GLOW_UNITS
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

        #self.runStepTimer()
        return self.scenario

    def addUnit(self, index, position, whiteFlag):
        self.scenario = []

        if whiteFlag:
            cardData = self.white_hand[index]
            del self.white_hand[index]
            unit = Unit(cardData)
            self.whiteUnitRow.insert (position, unit)
            client = self.getWhiteId()
            price = self.white_step_price - cardData["price"]
            self.white_step_price = price
            rowLength = len (self.whiteUnitRow)
        else:
            cardData = self.black_hand[index]
            del self.black_hand[index]
            unit = Unit(cardData)
            self.blackUnitRow.insert (position, unit)
            client = self.getBlackId()
            price = self.black_step_price - cardData["price"]
            self.black_step_price = price
            rowLength = len (self.blackUnitRow)

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
        action['endAnimationFlag'] = False
        self.scenario.append (action)

        action = {}
        action['type'] = Action.SORT_DECK
        action['client'] = client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

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

            if mask['count'] > 0:
                self.selected_unit = unit

                logger.debug ('initSelectedEptitudes')

                self.selectMode = True

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


        action = {}
        action['type'] = Action.PLAY_CARD_UNIT
        action['client'] = client
        action['unit'] = unit.getCardData()
        action['position'] = position
        action['endAnimationFlag'] = True
        action['cardIndex'] = index
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

        if rowLength < 7:
            action = {}
            action['type'] = Action.GLOW_CARDS
            action['client'] = client
            action['endAnimationFlag'] = False
            self.scenario.append(action)


        self.controller = Controller()
        self.controller.setMatch(self)
        self.controller.setScenario(self.scenario)
        self.controller.setClient(client)
        self.controller.setWhiteFlag(whiteFlag)
        self.controller.addUnit(unit)

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

        if rowLength < 7:
            action = {}
            action['type'] = Action.GLOW_CARDS
            action['client'] = client
            action['endAnimationFlag'] = False
            self.scenario.append(action)

        self.controller = Controller()
        self.controller.setMatch(self)
        self.controller.setScenario(self.scenario)
        self.controller.setClient(client)
        self.controller.setWhiteFlag(whiteFlag)
        self.controller.addUnit(self.selected_unit)

        self.selectMode = False

        return self.scenario

    def cancelSelect (self, whiteFlag):

        cardData = self.selected_unit.cardData

        if whiteFlag:
            hand = self.white_hand
            row = self.whiteUnitRow
            client = self.getWhiteId()
            price = self.white_step_price + cardData['price']
            self.white_step_price = price
        else:
            hand = self.black_hand
            row = self.blackUnitRow
            client = self.getBlackId()
            price = self.black_step_price + cardData['price']
            self.black_step_price = price

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
        action['card'] = cardData
        scenario.append (action)

        action = {}
        action['type'] = Action.STEP_PRICE
        action['client'] = client
        action['price'] = price
        action['endAnimationFlag'] = False
        scenario.append (action)

        action = {}
        action['type'] = Action.UNBLOCK_DECK
        action['client'] = client
        action['endAnimationFlag'] = False
        scenario.append(action)

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

        # checkProvocation
        if self.notValidProvocation(whiteFlag, targetUnit):
             self.scenario = []
             action = {}
             action['type'] = Action.PROVOCATION_EXCEPTION
             action['client'] = client
             action['endAnimationFlag'] = False
             self.scenario.append(action)
             return self.scenario

        attackValue = attackUnit.getTotalAttack()
        healthValue = targetUnit.getHealth()
        newHealthValue = healthValue - attackValue
        targetUnit.setHealth(newHealthValue)

        attackValue = targetUnit.getTotalAttack()
        healthValue = attackUnit.getHealth()
        newHealthValue = healthValue - attackValue
        attackUnit.setHealth(newHealthValue)

        self.scenario = []

        action = {}
        action['type'] = Action.ATTACK
        action['client'] = client
        action['endAnimationFlag'] = True
        action['initiatorIndex'] = initiatorIndex
        action['targetIndex'] = targetIndex
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

        action = {}
        action['type'] = Action.ATTACK_COMPLETE
        action['client'] = client
        action['endAnimationFlag'] = True
        self.scenario.append(action)

        #logger.debug ('attackUnit.health:%s' % attackUnit.getHealth())
        if attackUnit.getHealth() <= 0:
                if whiteFlag:
                     del self.whiteUnitRow[initiatorIndex]
                else:
                    del self.blackUnitRow[initiatorIndex]

                #logger.debug ('addAction::attack_token_death')
                action = {}
                action['type'] = Action.ATTACK_TOKEN_DEATH
                action['client'] = client
                action['endAnimationFlag'] = True
                action['initiatorIndex'] = initiatorIndex
                self.scenario.append(action)

        if targetUnit.getHealth() <=0:
                if targetIndex >= 0:
                    if whiteFlag:
                         del self.blackUnitRow[targetIndex]
                    else:
                         del self.whiteUnitRow[targetIndex]

                    #logger.debug ('addAction::target_token_death')
                    action = {}
                    action['type'] = Action.TARGET_TOKEN_DEATH
                    action['client'] = client
                    action['endAnimationFlag'] = True
                    action['targetIndex'] = targetIndex
                    self.scenario.append(action)
                else:
                    #logger.debug ('addAction::opponent_hero_death')
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

                    action = {}
                    action['type'] = Action.OPPONENT_HERO_DEATH
                    action['client'] = client
                    action['endAnimationFlag'] = True
                    self.scenario.append(action)


        list = []
        for item in self.whiteUnitRow:
            list.append (item.getTitle())

        list = []
        for item in self.blackUnitRow:
            list.append (item.getTitle())

        return self.scenario

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


        return levelList

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
            if item.isProvocator():
                flag = True
        return flag

    def validateSelectedEptitudes (self, eptitudes):
        selectedFlag = False
        for eptitude in eptitudes:
            if eptitude.level == EptitudeLevel.SELECTED:
                selectedFlag = True
        return selectedFlag

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



























