__author__ = 'RIK'
import logging
logger =  logging.getLogger('game_handler')

from game.logic.action import Action
from card.models import Card
from game.logic.unit import Unit
from card.models import SubRace, Race



class EptitudeAttachment():
    ASSOCIATE = 0
    OPPONENT = 1
    ALL = 2

class EptitudeLevel():
    SELF = 0
    All = 1
    RANDOM = 2
    SELECTED = 3
    LEFT_NEIGHBOR = 4
    RIGHT_NEIGHBOR = 5
    NEIGHBORS = 6
    HERO = 7
    DECK = 8
    HAND = 9
    UNIT_CARDS = 10
    SPELL_CARDS = 11
    LAST_ATTACKED = 12
    LAST_ATTACKED_UNIT = 13
    INITIATOR = 14
    INITIATOR_UNIT = 15

class EptitudeType():
    JERK = 1
    DOUBLE_ATTACK = 2
    PASSIVE_ATTACK = 3
    PROVOCATION = 4
    INCREASE_ATTACK = 5
    INCREASE_HEALTH = 6
    DECREASE_ATTACK = 7
    DECREASE_HEALTH = 8
    CHANGE_ATTACK_TILL = 9
    CHANGE_HEALTH_TILL = 10
    FULL_HEALTH = 11
    DUMBNESS = 12
    TREATMENT = 13
    PICK_CARD = 14
    BACK_CARD_TO_HAND = 15
    KILL = 16
    SHADOW = 17
    FREEZE = 18
    NEW_UNIT = 19
    SHIELD = 20
    INCREASE_ATTACK_MIXIN = 21
    DECREASE_ATTACK_MIXIN = 22
    CAN_NOT_ATTACK = 23
    REPLACE_ATTACK_HEALTH = 24
    SALE = 25
    INCREASE_SPELL = 26
    DECREASE_SPELL = 27
    SPELL_INVISIBLE = 28
    MASSIVE_ATTACK = 29
    INCREASE_ATTACK_AND_HEALTH = 30
    INCREASE_HEALTH_MIXIN = 31
    DECREASE_HEALTH_MIXIN = 32
    ENTICE_UNIT = 33
    NEW_SPELL = 34
    COPY_UNIT = 35
    UNIT_CONVERTION = 36

class EptitudePeriod ():
    START_STEP = 0
    END_STEP = 1
    SELF_PLACED = 2

class Controller ():

    def __init__(self):
        self.period_START_STEP = 0
        self.period_END_STEP = 1
        self.period_SELF_PLACED = 2

    def setScenario (self, scenario):
        self.scenario = scenario

    def setMatch (self, match):
        self.match = match

    def setClient (self, client):
        self.client = client

    def setWhiteFlag(self, flag):
        self.whiteFlag = flag

    def addUnit(self, unit):
        self.eptitudes = unit.eptitudes[:]
        self.unit = unit
        self.activate(EptitudePeriod.SELF_PLACED)

    def activate (self, period):
        logger.debug ('CardController::activate')

        if len(self.eptitudes):
            eptitude = self.eptitudes[0]
            del  self.eptitudes[0]

            logger.debug ('eptitude.period: %s' % eptitude.period)
            if period == eptitude.period:

                targets = self.match.getLevelTargets (self.unit, eptitude, self.whiteFlag)

                if eptitude.type == EptitudeType.JERK:
                     logger.debug ('eptitude.type: JERK')
                     for target in targets:
                         target.jerk = True

                     action = {}
                     action['type'] = Action.JERK
                     action['client'] = self.client
                     action['endAnimationFlag'] = False
                     clientTargets = self.match.getTargetsIndexes(targets, self.whiteFlag)
                     action["targets"] = clientTargets
                     self.scenario.append (action)


                if eptitude.type == EptitudeType.DOUBLE_ATTACK:
                     logger.debug ('eptitude.type: DOUBLE_ATTACK')

                if eptitude.type == EptitudeType.PASSIVE_ATTACK:
                     logger.debug ('eptitude.type: PASSIVE_ATTACK')
                     self.passive_attack (self.unit, targets, eptitude)

                if eptitude.type == EptitudeType.PROVOCATION:
                     logger.debug ('eptitude.type: PROVOCATION')
                     for target in targets:
                         target.provocation = True

                     action = {}
                     action['type'] = Action.PROVOCATION
                     action['client'] = self.client
                     action['endAnimationFlag'] = False
                     clientTargets = self.match.getTargetsIndexes(targets, self.whiteFlag)
                     action["targets"] = clientTargets
                     self.scenario.append (action)


                if eptitude.type == EptitudeType.INCREASE_ATTACK:
                     logger.debug ('eptitude.type: INCREASE_ATTACK')

                if eptitude.type == EptitudeType.INCREASE_HEALTH:
                    logger.debug ('eptitude.type: INCREASE_HEALTH')

                if eptitude.type == EptitudeType.DECREASE_ATTACK:
                    logger.debug ('eptitude.type: DECREASE_ATTACK')

                if eptitude.type == EptitudeType.DECREASE_HEALTH:
                    logger.debug ('eptitude.type: DECREASE_HEALTH')

                if eptitude.type == EptitudeType.CHANGE_ATTACK_TILL:
                    logger.debug ('eptitude.type: CHANGE_ATTACK_TILL')

                if eptitude.type == EptitudeType.CHANGE_HEALTH_TILL:
                    logger.debug ('eptitude.type: DECREASE_HEALTH')

                if eptitude.type == EptitudeType.FULL_HEALTH:
                    logger.debug ('eptitude.type: FULL_HEALTH')

                if eptitude.type == EptitudeType.DUMBNESS:
                    logger.debug ('eptitude.type: DUMBNESS')

                if eptitude.type == EptitudeType.TREATMENT:
                    logger.debug ('eptitude.type: TREATMENT')

                if eptitude.type == EptitudeType.PICK_CARD:
                    logger.debug ('eptitude.type: PICK CARD')
                    self.pick_card(eptitude)

                if eptitude.type == EptitudeType.BACK_CARD_TO_HAND:
                    logger.debug ('eptitude.type: BACK_CARD_TO_HAND')

                if eptitude.type == EptitudeType.KILL:
                    logger.debug ('eptitude.type: KILL')

                if eptitude.type == EptitudeType.SHADOW:
                    logger.debug ('eptitude.type: SHADOW')

                if eptitude.type == EptitudeType.FREEZE:
                    logger.debug ('eptitude.type: FREEZE')

                if eptitude.type == EptitudeType.NEW_UNIT:
                    logger.debug ('eptitude.type: NEW_UNIT')
                    self.new_unit (self.unit, eptitude)

                if eptitude.type == EptitudeType.INCREASE_ATTACK_MIXIN:
                    logger.debug ('eptitude.type: INCREASE_ATTACK_MIXIN')
                    self.increase_attack_mixin (eptitude, targets)


                if eptitude.type == EptitudeType.DECREASE_ATTACK_MIXIN:
                    logger.debug ('eptitude.type: DECREASE_ATTACK_MIXIN')

                if eptitude.type == EptitudeType.CAN_NOT_ATTACK:
                    logger.debug ('eptitude.type: CAN_NOT_ATTACK')

                if eptitude.type == EptitudeType.REPLACE_ATTACK_HEALTH:
                    logger.debug ('eptitude.type: REPLACE_ATTACH_HEALTH')

                if eptitude.type == EptitudeType.SALE:
                    logger.debug ('eptitude.type: SALE')

                if eptitude.type == EptitudeType.INCREASE_SPELL:
                    logger.debug ('eptitude.type: INCREASE_SPELL')

                if eptitude.type == EptitudeType.DECREASE_SPELL:
                    logger.debug ('eptitude.type: DECREASE_SPELL')

                if eptitude.type == EptitudeType.SPELL_INVISIBLE:
                    logger.debug ('eptitude.type: SPELL_INVISIBLE')

                if eptitude.type == EptitudeType.MASSIVE_ATTACK:
                    logger.debug ('eptitude.type: MASSIVE_ATTACK')

                if eptitude.type == EptitudeType.INCREASE_ATTACK_AND_HEALTH:
                    logger.debug ('eptitude.type: INCREASE_ATTACK_AND_HEALTH')
                    power = eptitude.power
                    for target in targets:
                        target.setAttack(target.getAttack() + power)
                        target.setHealth(target.getHealth() + power)
                        target.setMaxHealth (target.getMaxHealth() + power)
                        action = {}
                        action['type'] = Action.INCREASE_ATTACK_AND_HEALTH
                        action['client'] = self.client
                        action['endAnimationFlag'] = True
                        action["power"] = power
                        targetAttachment = self.match.initAttachment (target, self.whiteFlag)
                        targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
                        action['targetIndex'] = targetIndex
                        action['targetAttachment'] = targetAttachment
                        self.scenario.append (action)

                if eptitude.type == EptitudeType.INCREASE_HEALTH_MIXIN:
                    logger.debug ('eptitude.type: INCREASE_HEALTH_MIXIN')

                if eptitude.type == EptitudeType.DECREASE_HEALTH_MIXIN:
                    logger.debug ('eptitude.type: DECREASE_HEALTH_MIXIN')

                if eptitude.type == EptitudeType.ENTICE_UNIT:
                    logger.debug ('eptitude.type: ENTICE_UNIT')

                if eptitude.type == EptitudeType.NEW_SPELL:
                    logger.debug ('eptitude.type: NEW_SPELL')

                if eptitude.type == EptitudeType.COPY_UNIT:
                    logger.debug ('eptitude.type: COPY_UNIT')

                if eptitude.type == EptitudeType.UNIT_CONVERTION:
                    logger.debug ('eptitude.type: UNIT_CONVERTION')

            self.activate(period)

    def passive_attack (self, unit, targets, eptitude):
        attackValue = eptitude.power
        for targetUnit in targets:

            healthValue = targetUnit.getHealth()
            newHealthValue = healthValue - attackValue
            targetUnit.setHealth(newHealthValue)

            initiatorAttachment = self.match.initAttachment (unit, self.whiteFlag)
            logger.debug ('initiatorAttachment: %s' % initiatorAttachment)
            initiatorIndex = self.match.initIndex (unit, initiatorAttachment, self.whiteFlag)
            logger.debug ('initiatorIndex: %s' % initiatorIndex)

            targetAttachment = self.match.initAttachment (targetUnit, self.whiteFlag)
            logger.debug ('targetAttachment: %s' % targetAttachment)
            targetIndex = self.match.initIndex (targetUnit, targetAttachment, self.whiteFlag)
            logger.debug ('targetIndex: %s' % targetIndex)

            action = {}
            action['type'] = Action.PASSIVE_ATTACK
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['initiatorAttachment'] = initiatorAttachment
            action['initiatorIndex'] = initiatorIndex
            action['targetIndex'] = targetIndex
            action['targetAttachment'] = targetAttachment
            self.scenario.append(action)

            action = {}
            action['type'] = Action.HEALTH_AFTER_PASSIVE_ATTACK
            action['client'] = self.client
            action['endAnimationFlag'] = False
            action['targetIndex'] = targetIndex
            action['targetAttachment'] = targetAttachment
            action["targetUnitHealth"] = targetUnit.getHealth()
            self.scenario.append(action)

            if targetUnit.getHealth() <=0:
                if targetIndex >= 0:
                    self.match.deleteUnit (targetIndex, targetAttachment, self.whiteFlag)
                    action = {}
                    action['type'] = Action.TOKEN_DEATH
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    action['targetIndex'] = targetIndex
                    action['targetAttachment'] = targetAttachment
                    self.scenario.append(action)
                else:
                    #logger.debug ('addAction::opponent_hero_death')
                    action = {}
                    action['type'] = Action.HERO_DEATH
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    action['targetAttachment'] = targetAttachment
                    self.scenario.append(action)

    def pick_card (self, eptitude):
        count = eptitude.power

        if self.whiteFlag:
            opponentFlag = False
        else:
            opponentFlag = True

        for i in range(count):
            attachment = eptitude.attachment
            if attachment == EptitudeAttachment.ASSOCIATE:

                card = self.match.getCard(self.whiteFlag)
                action = {}
                action['type'] = Action.PICK_CARD
                action['client'] = self.client
                action['attachment'] = 1
                action['card'] = card
                action['endAnimationFlag'] = True
                self.scenario.append(action)

            elif attachment == EptitudeAttachment.OPPONENT:

                card = self.match.getCard(opponentFlag)
                action = {}
                action['type'] = Action.PICK_CARD
                action['client'] = self.client
                action['attachment'] = 0
                action['card'] = card
                action['endAnimationFlag'] = True
                self.scenario.append(action)

            elif attachment == EptitudeAttachment.ALL:

                card = self.match.getCard(self.whiteFlag)
                action = {}
                action['type'] = Action.PICK_CARD
                action['client'] = self.client
                action['attachment'] = 1
                action['card'] = card
                action['endAnimationFlag'] = True
                self.scenario.append(action)
                card2 = self.match.getCard(opponentFlag)

                action = {}
                action['type'] = Action.PICK_CARD
                action['client'] = self.client
                action['attachment'] = 0
                action['card'] = card2
                action['endAnimationFlag'] = True
                self.scenario.append(action)


    def new_unit (self, unit, eptitude):
        count = eptitude.power

        if self.whiteFlag:
            playerRow = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
        else:
            playerRow = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow

        logger.debug ('new_unit count:%s' % count)

        for i in range(count):

            # определяемся с юнитом
            try:
                subraceId = eptitude.subrace
                subrace = SubRace.objects.get(id=subraceId)
                unitCard = random.choice(Card.objects.filter(subrace=subrace))
            except: pass
            try:
                raceId = eptitude.race
                race = SubRace.objects.get(id=raceId)
                unitCard = random.choice(Card.objects.filter(race=race))
            except: pass
            try:
                cardId = eptitude.unit
                unitCard = Card.objects.get(id=cardId)
            except: pass

            targetRows = []
            # определяемся с рядом
            if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
                # уточняем общее количество в ряду
                if len(playerRow) < 7:
                    targetRows.append (playerRow)
            elif eptitude.attachment == EptitudeAttachment.OPPONENT:
                if len(opponentRow) < 7:
                    targetRows.append (opponentRow)
            else:
                if len(playerRow) < 7:
                    targetRows.append (playerRow)
                if len(opponentRow) < 7:
                    targetRows.append (opponentRow)


            # уточняем индексы
            try:
                playerIndex = playerRow.index (unit) + 1
            except:
                playerIndex = unit.index
            opponentIndex = len(opponentRow)

            # добавляем в ряд
            cardData = self.match.getUnitCardData(unitCard)
            for row in targetRows:
                targetUnit = Unit(cardData)
                if row == playerRow:
                    row.insert (playerIndex, targetUnit)
                    # записываем в сценарий
                    action = {}
                    action['type'] = Action.NEW_UNIT
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    action['attachment'] = 1
                    action['index'] = playerIndex
                    action['cardData'] = cardData
                    self.scenario.append(action)
                    logger.debug ('append scenario action : new_unit')

                else:
                    row.insert (opponentIndex, targetUnit)
                    # записываем в сценарий
                    action = {}
                    action['type'] = Action.NEW_UNIT
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    action['attachment'] = 0
                    action['index'] = opponentIndex
                    action['cardData'] = cardData
                    self.scenario.append(action)
                    logger.debug ('append scenario action : new_unit')

    def increase_attack_mixin (self, targets, eptitude):
        power = eptitude.power
        for target in targets:
            attachment = self.match.initAttachment (target, self.whiteFlag)
            index = self.match.initIndex (target, attachment, self.whiteFlag)

            mixinAttack = target.getDynamicAttack()
            mixinAttack += power
            target.setDynamicAttack (mixinAttack)
            action = {}
            action['type'] = Action.ATTACK_MIXIN
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['attachment'] = attachment
            action['power'] = power
            action['index'] = index
            self.scenario.append(action)












