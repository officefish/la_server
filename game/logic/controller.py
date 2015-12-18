__author__ = 'RIK'
import logging
logger =  logging.getLogger('game_handler')

import random

from game.logic.cardController import CardController


from game.logic.action import Action
from card.models import Card
from game.logic.unit import Unit, HeroUnit
from card.models import SubRace, Race
from game.logic.constants import EptitudePeriod, EptitudeCondition, EptitudeLevel, EptitudeAttachment, EptitudeType, CardType
from group.models import Group
from  weapon.models import Weapon

class Controller ():

    def __init__(self):
        self.id = random.randint(0, 10000)

    def setScenario (self, scenario):
        self.scenario = scenario

    def setMatch (self, match):
        self.match = match

    def setClient (self, client):
        self.client = client

    def setWhiteFlag(self, flag):
        self.whiteFlag = flag

    def spellToTarget(self, unit):
        logger.debug('Controller::spellToTarget')
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        logger.debug(self.eptitudes)
        self.activate(EptitudePeriod.ACTIVATE_SPELL_TO_TARGET)

    def spell(self, unit):
        logger.debug('Controller::spell')
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.ACTIVATE_SPELL)

    def activateAchieve(self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.ACTIVATE_ACHIEVE)

    def activateActive(self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.ACTIVATE_ACTIVE)

    def preAttack(self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.PRE_ATTACK)

    def opponentPreAttack(self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.OPPONENT_PRE_ATTACK)

    def enticeAssociate(self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.ASSOCIATE_ENTICE)

    def enticeOpponent(self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.OPPONENT_ENTICE)

    def addUnit(self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.SELF_PLACED)

    def activateEptitude(self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.ACTIVATED)

    def attack(self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.ATTACK)

    def isAttacked(self, unit):
        self.unit = unit
        if isinstance(unit, Unit):
            self.eptitudes = unit.eptitudes[:]
            self.activate(EptitudePeriod.IS_ATTACKED)

    def associateSpell (self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.ASSOCIATE_SPELL)

    def opponentSpell (self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.OPPONENT_SPELL)

    def allSpell (self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.ALL_SPELL)

    def endStep (self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.END_STEP)

    def opponentEndStep(self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.OPPONENT_END_STEP)

    def startStep (self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.START_STEP)

    def opponentStartStep (self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.OPPONENT_START_STEP)

    def unitPlaced (self, unit):
        self.match.setLastPlaced(unit)

        try:
            self.match.whiteUnitRow.index(unit)
            playerRow = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
        except:
            playerRow = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow

        # активируем (EptitudePeriod.ASSOCIATE_PLACED)
        for item in playerRow:
            if item != unit:
                self.unit = item
                self.eptitudes = item.eptitudes[:]
                self.activate (EptitudePeriod.ASSOCIATE_PLACED)
                self.eptitudes = item.eptitudes[:]
                self.activate(EptitudePeriod.ASSOCIATE_RACE_PLACED)

        for item in opponentRow:
            self.unit = item
            self.eptitudes = item.eptitudes[:]
            self.activate (EptitudePeriod.OPPONENT_PLACED)
            self.eptitudes = item.eptitudes[:]
            self.activate(EptitudePeriod.OPPONENT_RACE_PLACED)


        for item in playerRow:
            if item != unit:
                self.unit = item
                self.eptitudes = item.eptitudes[:]
                self.activate(EptitudePeriod.ALL_PLACED)
                self.eptitudes = item.eptitudes[:]
                self.activate(EptitudePeriod.ALL_RACE_PLACED)

        for item in opponentRow:
            self.unit = item
            self.eptitudes = item.eptitudes[:]
            self.activate(EptitudePeriod.ALL_PLACED)
            self.eptitudes = item.eptitudes[:]
            self.activate(EptitudePeriod.ALL_RACE_PLACED)

    def newCard (self, unit) :
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.NEW_CARD_IN_HAND)

    def newPlayerCard (self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.NEW_PLAYER_CARD_IN_HAND)

    def newOpponentCard (self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.NEW_OPPONENT_CARD_IN_HAND)

    def configureUnit (self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.configure()


    def playCard (self, unit):
        self.match.setLastPlaced(unit)

        try:
            self.match.whiteUnitRow.index(unit)
            playerRow = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
        except:
            playerRow = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow

        # активируем (EptitudePeriod.ASSOCIATE_PLACED)
        for item in playerRow:
            if item != unit:
                self.unit = item
                self.eptitudes = item.eptitudes[:]
                self.activate (EptitudePeriod.ASSOCIATE_PLAY_CARD)


        for item in opponentRow:
            self.unit = item
            self.eptitudes = item.eptitudes[:]
            self.activate(EptitudePeriod.OPPONENT_PLAY_CARD)


        for item in playerRow:
            if item != unit:
                self.unit = item
                self.eptitudes = item.eptitudes[:]
                self.activate(EptitudePeriod.ALL_PLAY_CARD)

        for item in opponentRow:
            self.unit = item
            self.eptitudes = item.eptitudes[:]
            self.activate(EptitudePeriod.ALL_PLAY_CARD)




    def woundUnit (self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.SELF_WOUND)

        try:
            self.match.whiteUnitRow.index(unit)
            playerRow = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
        except:
            playerRow = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow

        # активируем (EptitudePeriod.ASSOCIATE_PLACED)
        for item in playerRow:
            if item != unit:
                self.unit = item
                self.eptitudes = item.eptitudes[:]
                self.activate (EptitudePeriod.ASSOCIATE_WOUND)

        for item in opponentRow:
            self.unit = item
            self.eptitudes = item.eptitudes[:]
            self.activate (EptitudePeriod.OPPONENT_WOUND)

        for item in playerRow:
            if item != unit:
                self.unit = item
                self.eptitudes = item.eptitudes[:]
                self.activate (EptitudePeriod.ALL_WOUND)

        for item in opponentRow:
            self.unit = item
            self.eptitudes = item.eptitudes[:]
            self.activate (EptitudePeriod.ALL_WOUND)


    def fullHealthUnit (self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        self.activate(EptitudePeriod.SELF_FULL_HEALTH)

    def removeUnit (self, unit):
        self.unit = unit
        self.eptitudes = unit.eptitudes[:]
        logger.debug ('die unit eptitudes len: %s' % len(self.eptitudes) )
        for eptitude in self.eptitudes:
            logger.debug('type:%s , period:%s' % (eptitude.type, eptitude.period))
        self.activate(EptitudePeriod.SELF_DIE)

        if self.containsDynamicEptitudes (unit):
            self.deactivateDynamic (unit)

        try:
            self.match.whiteUnitRow.index(unit)
            playerRow = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
        except:
            playerRow = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow

        # активируем (EptitudePeriod.ASSOCIATE_PLACED)
        for item in playerRow:
            if item != unit:
                self.unit = item
                self.eptitudes = item.eptitudes[:]
                if unit.whiteFlag == item.whiteFlag:
                    self.activate (EptitudePeriod.ASSOCIATE_DIE)
                else:
                    self.activate (EptitudePeriod.OPPONENT_DIE)

        for item in opponentRow:
            self.unit = item
            self.eptitudes = item.eptitudes[:]
            if unit.whiteFlag == item.whiteFlag:
                self.activate (EptitudePeriod.ASSOCIATE_DIE)
            else:
                self.activate (EptitudePeriod.OPPONENT_DIE)

        for item in playerRow:
            if item != unit:
                self.unit = item
                self.eptitudes = item.eptitudes[:]
                self.activate (EptitudePeriod.ALL_DIE)

        for item in opponentRow:
            self.unit = item
            self.eptitudes = item.eptitudes[:]
            self.activate (EptitudePeriod.ALL_DIE)

    def containsDynamicEptitudes (self, unit):
        flag = False
        for eptitude in unit.eptitudes:
            if eptitude.dynamic:
                flag = True
        return flag

    def deactivateDynamic (self, unit):

        for eptitude in unit.eptitudes:

            if eptitude.dynamic:
                targets = self.match.getLevelTargets (unit, eptitude, unit.whiteFlag)

                if eptitude.type == EptitudeType.INCREASE_ATTACK_MIXIN:
                      logger.debug ('decrease_attack_mixin::targets.length: %s' % (len(targets)))
                      self.decrease_attack_mixin(targets, eptitude)

                if eptitude.type == EptitudeType.DECREASE_ATTACK_MIXIN:
                      logger.debug ('increase_attack_mixin::targets.length: %s' % (len(targets)))
                      self.increase_attack_mixin(targets, eptitude)


                if eptitude.type == EptitudeType.INCREASE_HEALTH_MIXIN:
                      logger.debug ('decrease_health_mixin::targets.length: %s' % (len(targets)))
                      self.decrease_health_mixin(targets, eptitude)

                if eptitude.type == EptitudeType.INCREASE_CARD_PRICE:
                      logger.debug ('deactivateDynamic: for %s cards' % (len(targets)))
                      self.decrease_card_price(unit, targets, eptitude)

                if eptitude.type == EptitudeType.DECREASE_CARD_PRICE:
                      logger.debug ('deactivateDynamic: for %s cards' % (len(targets)))
                      self.increase_card_price(unit, targets, eptitude)

                if eptitude.type == EptitudeType.INCREASE_CARD_PRICE_MIXIN:
                     logger.debug ('deactivateDynamic: for %s cards' % (len(targets)))
                     self.decrease_card_price_mixin(unit, targets, eptitude)

                if eptitude.type == EptitudeType.DECREASE_CARD_PRICE_MIXIN:
                      logger.debug ('deactivateDynamic: for %s cards' % (len(targets)))
                      self.increase_card_price_mixin(unit, targets, eptitude)

                if eptitude.type == EptitudeType.INCREASE_SPELL:
                    logger.debug ('deactivateDynamic: INCREASE_SPELL')
                    self.decreaseSpell (targets, eptitude)


                if eptitude.type == EptitudeType.CAN_NOT_ATTACK:
                      logger.debug ('deactivateDynamic: for %s cards' % (len(targets)))
                      for target in targets:
                         target.canAttack = True
                         if target.doubleAttack:
                             target.stepAttack = 2
                         else:
                             target.stepAttack = 1

                      if self.whiteFlag:
                          player = self.match.whiteHeroUnit
                          row = self.match.whiteUnitRow
                      else:
                          player = self.match.blackHeroUnit
                          row = self.match.blackUnitRow

                      if player == self.match.activePlayer:

                           action = {}
                           action['type'] = Action.ATTACK_AVAILABLE
                           action['client'] = self.client
                           action['endAnimationFlag'] = False
                           units = []
                           for unit in row:
                                if unit.stepAttack > 0 and \
                                unit.canAttack and \
                                unit.attack > 0 and \
                                unit.freeze == False and \
                                unit.replaceFlag == False:
                                     units.append (row.index(unit))

                           action['unitList'] = units
                           self.scenario.append(action)

                           action = {}
                           action['type'] = Action.GLOW_UNITS
                           action['client'] = self.client
                           action['endAnimationFlag'] = False
                           self.scenario.append(action)



    def activateDynamic (self, unit):
         for eptitude in unit.eptitudes:

            if eptitude.dynamic:
                targets = self.match.getLevelTargets (unit, eptitude, unit.whiteFlag)

                if eptitude.type == EptitudeType.INCREASE_ATTACK_MIXIN:
                      logger.debug ('activateDynamic: for %s cards' % (len(targets)))
                      self.increase_attack_mixin(targets, eptitude)

                if eptitude.type == EptitudeType.INCREASE_HEALTH_MIXIN:
                      logger.debug ('activateDynamic: for %s cards' % (len(targets)))
                      self.increase_health_mixin(targets, eptitude)

                if eptitude.type == EptitudeType.INCREASE_CARD_PRICE:
                      logger.debug ('activateDynamic: for %s cards' % (len(targets)))
                      self.increase_card_price(unit, targets, eptitude)

                if eptitude.type == EptitudeType.DECREASE_CARD_PRICE:
                      logger.debug ('activateDynamic: for %s cards' % (len(targets)))
                      self.decrease_card_price(unit, targets, eptitude)

                if eptitude.type == EptitudeType.INCREASE_CARD_PRICE_MIXIN:
                     logger.debug ('activateDynamic: for %s cards' % (len(targets)))
                     self.increase_card_price_mixin(unit, targets, eptitude)

                if eptitude.type == EptitudeType.DECREASE_CARD_PRICE_MIXIN:
                      logger.debug ('activateDynamic: for %s cards' % (len(targets)))
                      self.decrease_card_price_mixin(unit, targets, eptitude)

                if eptitude.type == EptitudeType.INCREASE_SPELL:
                    self.increaseSpell (targets, eptitude)

                if eptitude.type == EptitudeType.CAN_NOT_ATTACK:
                      logger.debug ('deactivateDynamic: for %s cards' % (len(targets)))
                      for target in targets:
                         target.canAttack = False
                      if self.whiteFlag:
                          player = self.match.whiteHeroUnit
                          row = self.match.whiteUnitRow
                      else:
                          player = self.match.blackHeroUnit
                          row = self.match.blackUnitRow

                      if player == self.match.activePlayer:

                           action = {}
                           action['type'] = Action.ATTACK_AVAILABLE
                           action['client'] = self.client
                           action['endAnimationFlag'] = False
                           units = []
                           for unit in row:
                                if unit.stepAttack > 0 and \
                                unit.canAttack and \
                                unit.attack > 0 and \
                                unit.freeze == False and \
                                unit.replaceFlag == False:
                                     units.append (row.index(unit))

                           action['unitList'] = units
                           self.scenario.append(action)

                           action = {}
                           action['type'] = Action.GLOW_UNITS
                           action['client'] = self.client
                           action['endAnimationFlag'] = False
                           self.scenario.append(action)


    def deactivateTempEptitudes (self, unit):
        tempEptitudes = []
        targets = [unit]
        for eptitude in unit.tempEptitudes:
            eptitude.lifecycle -= 1
            if eptitude.lifecycle > 0:
               tempEptitudes.append(eptitude)
            if eptitude.lifecycle == 0:
                if eptitude.type == EptitudeType.ENTICE_UNIT:
                    logger.debug ('deactivateTempEptitudes: ENTICE_UNIT')
                    logger.debug (eptitude.target)
                    index = -1
                    try:
                        index = self.match.whiteUnitRow.index(eptitude.target)
                    except:
                        pass
                    try:
                        index = self.match.blackUnitRow.index(eptitude.target)
                    except:
                        pass
                    if index > - 1:
                        self.entice_unit([eptitude.target], eptitude)

                if eptitude.type == EptitudeType.INCREASE_ATTACK:
                    self.decrease_attack(targets, eptitude)
                if eptitude.type == EptitudeType.SHADOW:
                    self.destroy_shadow(targets)
                if eptitude.type == EptitudeType.INCREASE_MANA:
                    logger.debug ('deactivateTempEptitudes: INCREASE_MANA')
                    self.decreaseMana(targets, eptitude)
                if eptitude.type == EptitudeType.DECREASE_MANA:
                    logger.debug ('deactivateTempEptitudes: DECREASE_MANA')
                    self.icreaseMana(targets, eptitude)
                if eptitude.type == EptitudeType.DOUBLE_ATTACK:
                    self.deactivateDoubleAttack(targets, eptitude)
            if eptitude.lifecycle < 0:
                # такая ситуация может возникнуть если привязать одну и ту же способность к нескольким юнитам
                # в этом случае мы игнорируем деактивацию, поскольку ранее она уже была деактивирована
                # пример: мана которая работает на один ход для обоих персонажей
                pass




        unit.tempEptitudes = tempEptitudes




    def configure(self):

        if len(self.eptitudes):
            eptitude = self.eptitudes[0]
            del  self.eptitudes[0]

            targets = self.match.getLevelTargets (self.unit, eptitude, self.whiteFlag)

            if eptitude.type == EptitudeType.JERK:
                for target in targets:
                    target.jerk = True

            if eptitude.type == EptitudeType.PROVOCATION:
                for target in targets:
                 target.provocation = True

            self.configure()





    def activate (self, period):
        #logger.debug ('Controller_%s::activate period %s' % (self.id, period))

        if len(self.eptitudes):
            eptitude = self.eptitudes[0]
            del  self.eptitudes[0]

            if period == eptitude.period:
                #logger.debug ('Eptitude period inited %s' % eptitude.period)

                if isinstance(eptitude.dependency, int):
                    if eptitude.dependency > 0:
                        logger.debug ('Init eptitude which has dependency from another eptitude: %s' % eptitude.dependency)
                        dependencyEptitude = self.unit.getEptitudeById(eptitude.dependency)
                        logger.debug ('dependency.activated: %s' % dependencyEptitude.activated)
                        if dependencyEptitude.activated == False:
                            self.activate(period)
                            return
                        else:
                            dependencyEptitude.activated = False


                # уточняем вероятность срабатывания способности
                if eptitude.probability < 100:
                    logger.debug('Probability of eptitude activation %s per.' % eptitude.probability)
                    probability = 100 / eptitude.probability
                    probability = int(round(probability))
                    probability = random.randint (1, probability)
                    if probability > 1:
                        logger.debug('Probability block eptitude activation')
                        self.activate(period)
                        return




                targets = self.match.getLevelTargets (self.unit, eptitude, self.whiteFlag)




                # race
                if eptitude.period == EptitudePeriod.ALL_RACE_PLACED:
                    try:
                        raceId = self.match.lastPlaced.race.id
                        if raceId != eptitude.race:
                            self.activate(period)
                            return
                    except:
                        self.activate(period)
                        return
                if eptitude.period == EptitudePeriod.ASSOCIATE_RACE_PLACED:
                    try:
                        raceId = self.match.lastPlaced.race.id
                        if raceId != eptitude.race:
                            self.activate(period)
                            return
                    except:
                        self.activate(period)
                        return
                if eptitude.period == EptitudePeriod.OPPONENT_RACE_PLACED:
                    try:
                        raceId = self.match.lastPlaced.race.id
                        if raceId != eptitude.race:
                            self.activate(period)
                            return
                    except:
                        self.activate(period)
                        return

                if len(targets) and eptitude.activate_widget == True:
                     if not self.unit.hasSelfDieEptitude():
                         logger.debug('Activate Widget for %s' % self.unit.cardData['title'])
                         targetAttachment = self.match.initAttachment (self.unit, self.whiteFlag)
                         targetIndex = self.match.initIndex (self.unit, targetAttachment, self.whiteFlag)
                         action = {}
                         action['type'] = Action.ACTIVATE_WIDGET
                         action['client'] = self.client
                         action['targetIndex'] = targetIndex
                         action['targetAttachment'] = targetAttachment
                         self.scenario.append(action)

                if eptitude.type == EptitudeType.JERK:
                     logger.debug ('eptitude.type: JERK')
                     jerkTargets = []
                     for target in targets:
                         target.jerk = True
                         if target.canAttack and target.attack > 0 and target.freeze == False and target.replaceFlag == False:
                             if target.stepAttack > 0:
                                jerkTargets.append(target)
                     action = {}
                     action['type'] = Action.JERK
                     action['client'] = self.client
                     action['endAnimationFlag'] = False
                     clientTargets = self.match.getTargetsCoord(jerkTargets, self.whiteFlag)
                     action["targets"] = clientTargets
                     self.scenario.append (action)


                if eptitude.type == EptitudeType.FLY:
                    logger.debug ('eptitude.type: FLY')
                    self.fly(targets, eptitude)

                if eptitude.type == EptitudeType.DOUBLE_ATTACK:
                     logger.debug ('eptitude.type: DOUBLE_ATTACK')
                     self.double_attack(targets, eptitude)


                if eptitude.type == EptitudeType.PASSIVE_ATTACK:
                     logger.debug ('eptitude.type: PASSIVE_ATTACK')
                     targets = self.match.getLevelTargets (self.unit, eptitude, self.unit.getWhiteFlag())
                     self.passive_attack (self.unit, targets, eptitude)

                if eptitude.type == EptitudeType.PASSIVE_ATTACK_SERIES:
                    logger.debug ('eptitude.type: PASSIVE_ATTACK_SERIES')
                    self.passive_attack_series(self.unit, eptitude)

                if eptitude.type == EptitudeType.PASSIVE_ATTACK_FOR_SEVERAL_TARGETS:
                    logger.debug ('eptitude.type: PASSIVE_ATTACK_FOR_SEVERAL_TARGETS')
                    self.passive_attack_for_several_targets(self.unit, eptitude)

                if eptitude.type == EptitudeType.PROVOCATION:
                     logger.debug ('eptitude.type: PROVOCATION')
                     self.provocation(targets)


                if eptitude.type == EptitudeType.INCREASE_ATTACK:
                    logger.debug ('eptitude.type: INCREASE_ATTACK')
                    self.increase_attack(targets, eptitude)

                if eptitude.type == EptitudeType.INCREASE_HEALTH:
                    logger.debug ('eptitude.type: INCREASE_HEALTH')
                    if len(targets):
                        eptitude.activated = True

                    power = eptitude.power
                    for target in targets:
                        target.setHealth(target.getHealth() + power)
                        target.setMaxHealth (target.getMaxHealth() + power)
                        action = {}
                        action['type'] = Action.CHANGE_HEALTH
                        action['client'] = self.client
                        action['endAnimationFlag'] = True
                        action["health"] = target.getHealth()
                        action['maxHealth'] = target.getMaxHealth()
                        targetAttachment = self.match.initAttachment (target, self.whiteFlag)
                        targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
                        action['index'] = targetIndex
                        action['attachment'] = targetAttachment
                        self.scenario.append (action)

                if eptitude.type == EptitudeType.ATTACK_EQUAL_TO_HEALTH:
                    logger.debug ('eptitude.type: ATTACK_EQUAL_TO_HEALTH')
                    self.attack_equals_to_health(targets, eptitude)

                if eptitude.type == EptitudeType.DECREASE_ATTACK:
                    logger.debug ('eptitude.type: DECREASE_ATTACK')

                if eptitude.type == EptitudeType.DECREASE_HEALTH:
                    logger.debug ('eptitude.type: DECREASE_HEALTH')
                    self.decreaseHealth(targets, eptitude)

                if eptitude.type == EptitudeType.CHANGE_ATTACK_TILL:
                    logger.debug ('eptitude.type: CHANGE_ATTACK_TILL')
                    power = eptitude.power
                    for target in targets:
                        target.setAttack(power)
                        action = {}
                        action['type'] = Action.INCREASE_ATTACK
                        action['client'] = self.client
                        action['endAnimationFlag'] = True
                        action["attack"] = target.getAttack()
                        targetAttachment = self.match.initAttachment (target, self.whiteFlag)
                        targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
                        action['index'] = targetIndex
                        action['attachment'] = targetAttachment
                        self.scenario.append (action)

                if eptitude.type == EptitudeType.MULTIPLY_ATTACK:
                    logger.debug ('eptitude.type: MULTIPLY_ATTACK')
                    self.multiplyAttack(targets, eptitude)

                if eptitude.type == EptitudeType.CHANGE_EXTRA_ATTACK_TILL:
                    logger.debug ('eptitude.type: CHANGE_EXTRA_ATTACK_TILL')
                    self.changeExtraAttackTill(targets, eptitude)

                if eptitude.type == EptitudeType.CHANGE_HEALTH_TILL:
                    logger.debug ('eptitude.type: CHANGE_HEALTH_TILL')
                    self.change_health_till(targets, eptitude)

                if eptitude.type == EptitudeType.FULL_HEALTH:
                    logger.debug ('eptitude.type: FULL_HEALTH')
                    self.full_health(targets, eptitude)

                if eptitude.type == EptitudeType.DUMBNESS:
                    logger.debug ('eptitude.type: DUMBNESS')
                    self.dumbness(targets, eptitude)

                if eptitude.type == EptitudeType.TREATMENT:
                    logger.debug ('eptitude.type: TREATMENT')
                    self.treatment(targets, eptitude)

                if eptitude.type == EptitudeType.PICK_CARD:
                    logger.debug ('eptitude.type: PICK CARD')
                    self.pick_card(targets, eptitude, eptitude.power)

                if eptitude.type == EptitudeType.PICK_CARD_TILL:
                    logger.debug ('eptitude.type: PICK_CARD_TILL')
                    self.pick_card_till(targets, eptitude)

                if eptitude.type == EptitudeType.PICK_CARD_DEPENDS_ON_WOUND_UNITS:
                    logger.debug ('eptitude.type: PICK_CARD_TILL')
                    self.pick_card_depends_on_wound_units(targets, eptitude)

                if eptitude.type == EptitudeType.PICK_CARDS_DEPENDS_ON_OPPONENT_CARDS_COUNT:
                    logger.debug ('PICK_CARDS_DEPENDS_ON_OPPONENT_CARDS_COUNT')
                    self.pick_card_depends_on_opponent_cards_count(targets, eptitude)

                if eptitude.type == EptitudeType.BACK_CARD_TO_HAND:
                    logger.debug ('eptitude.type: BACK_CARD_TO_HAND')
                    self.beckCardToHand(targets, eptitude)

                if eptitude.type == EptitudeType.BACK_SEVERAL_TOKENS_TO_HAND:
                    logger.debug ('eptitude.type: BACK_SEVERAL_TOKENS_TO_HAND')
                    self.backSeveralTokensToHand(targets, eptitude)

                if eptitude.type == EptitudeType.KILL:
                    logger.debug ('eptitude.type: KILL')
                    self.kill(self.unit, targets, eptitude)

                if eptitude.type == EptitudeType.MASSIVE_KILL:
                    logger.debug ('eptitude.type: MASSIVE_KILL')
                    self.massive_kill(targets, eptitude)

                if eptitude.type == EptitudeType.SHADOW:
                    logger.debug ('eptitude.type: SHADOW')
                    for target in targets:
                         target.shadow = True
                         action = {}
                         action['type'] = Action.SHADOW
                         action['client'] = self.client
                         targetAttachment = self.match.initAttachment (target, self.whiteFlag)
                         targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
                         action['index'] = targetIndex
                         action['attachment'] = targetAttachment
                         action['endAnimationFlag'] = False
                         self.scenario.append (action)

                if eptitude.type == EptitudeType.FREEZE_ATTACK:
                    logger.debug ('eptitude.type: FREEZE_ATTACK')
                    targets = self.match.getLevelTargets (self.unit, eptitude, self.unit.getWhiteFlag())
                    self.freeze_attack (self.unit, targets, eptitude)

                if eptitude.type == EptitudeType.FREEZE:
                    logger.debug ('eptitude.type: FREEZE')
                    targets = self.match.getLevelTargets (self.unit, eptitude, self.unit.getWhiteFlag())
                    self.freeze (targets, eptitude)

                if eptitude.type == EptitudeType.NEW_UNIT:
                    logger.debug ('eptitude.type: NEW_UNIT')
                    self.new_unit (self.unit, targets, eptitude)

                if eptitude.type == EptitudeType.REBIRTH:
                    logger.debug ('eptitude.type: REBIRTH')
                    self.rebirth (targets, eptitude)

                if eptitude.type == EptitudeType.SHIELD:
                     logger.debug ('eptitude.type: SHIELD')
                     self.shield(targets)

                if eptitude.type == EptitudeType.INCREASE_ATTACK_MIXIN:
                    logger.debug ('eptitude.type: INCREASE_ATTACK_MIXIN')
                    self.increase_attack_mixin (targets, eptitude)

                if eptitude.type == EptitudeType.INCREASE_HEALTH_MIXIN:
                    logger.debug ('eptitude.type: INCREASE_HEALTH_MIXIN')
                    self.increase_health_mixin(targets, eptitude)

                if eptitude.type == EptitudeType.DECREASE_ATTACK_MIXIN:
                    logger.debug ('eptitude.type: DECREASE_ATTACK_MIXIN')
                    self.decrease_attack_mixin(targets, eptitude)

                if eptitude.type == EptitudeType.CAN_NOT_ATTACK:
                    logger.debug ('eptitude.type: CAN_NOT_ATTACK')
                    for target in targets:
                         target.canAttack = False

                if eptitude.type == EptitudeType.REPLACE_ATTACK_HEALTH:
                    logger.debug ('eptitude.type: REPLACE_ATTACH_HEALTH')

                if eptitude.type == EptitudeType.SALE:
                    logger.debug ('eptitude.type: SALE')

                if eptitude.type == EptitudeType.INCREASE_SPELL:
                    logger.debug ('eptitude.type: INCREASE_SPELL')
                    self.increaseSpell (targets, eptitude)


                if eptitude.type == EptitudeType.DECREASE_SPELL:
                    logger.debug ('eptitude.type: DECREASE_SPELL')
                    self.decreaseSpell(targets, eptitude)


                if eptitude.type == EptitudeType.SPELL_INVISIBLE:
                    logger.debug ('eptitude.type: SPELL_INVISIBLE')
                    self.spellInvisible(targets)

                if eptitude.type == EptitudeType.MASSIVE_ATTACK:
                    logger.debug ('eptitude.type: MASSIVE_ATTACK')
                    targets = self.match.getLevelTargets (self.unit, eptitude, self.unit.getWhiteFlag())
                    self.massive_attack(self.unit, targets, eptitude)

                if eptitude.type == EptitudeType.MASSIVE_ATTACK_DEPENDS_ON_TARGET_ATTACK_VALUE:
                    logger.debug ('eptitude.type: MASSIVE_ATTACK_DEPENDS_ON_TARGET_ATTACK_VALUE')
                    self.massive_attack_depends_on_target_attack_value(targets, eptitude)

                if eptitude.type == EptitudeType.MASSIVE_ATTACK_DEPENDS_ON_UNIT_ATTACK_VALUE:
                    logger.debug ('eptitude.type: MASSIVE_ATTACK_DEPENDS_ON_UNIT_ATTACK_VALUE')
                    targets = self.match.getLevelTargets (self.unit, eptitude, self.unit.getWhiteFlag())
                    eptitude.power = self.match.spellTarget.getTotalAttack()
                    self.massive_attack(self.unit, targets, eptitude)

                if eptitude.type == EptitudeType.INCREASE_ATTACK_AND_HEALTH:
                    logger.debug ('eptitude.type: INCREASE_ATTACK_AND_HEALTH')
                    power = eptitude.power
                    for target in targets:
                        noAttackFlag = False
                        if target.getAttack() == 0 and target.stepCount > 0 and self.whiteFlag == target.whiteFlag:
                            noAttackFlag = True

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

                        if noAttackFlag:
                             action = {}
                             action['type'] = Action.ATTACK_AVAILABLE
                             action['client'] = self.client
                             action['endAnimationFlag'] = False
                             da_units = []
                             da_units.append (target.row.index(target))
                             action['unitList'] = da_units
                             self.scenario.append(action)

                             action = {}
                             action['type'] = Action.GLOW_UNITS
                             action['client'] = self.client
                             action['endAnimationFlag'] = False
                             self.scenario.append(action)

                if eptitude.type == EptitudeType.DECREASE_HEALTH_MIXIN:
                    logger.debug ('eptitude.type: DECREASE_HEALTH_MIXIN')

                if eptitude.type == EptitudeType.ENTICE_UNIT:
                    logger.debug ('eptitude.type: ENTICE_UNIT')
                    self.entice_unit(targets, eptitude)

                if eptitude.type == EptitudeType.NEW_SPELL:
                    logger.debug ('eptitude.type: NEW_SPELL')

                if eptitude.type == EptitudeType.COPY_UNIT:
                    logger.debug ('eptitude.type: COPY_UNIT')
                    self.copy_unit (targets, eptitude)

                if eptitude.type == EptitudeType.UNIT_CONVERTION:
                    logger.debug ('eptitude.type: UNIT_CONVERTION')
                    self.unit_convertion(targets, eptitude)

                if eptitude.type == EptitudeType.DEFAULT_ATTACK:
                    logger.debug ('eptitude.type: DEFAULT_ATTACK')
                    self.default_attack(targets, eptitude)

                if eptitude.type == EptitudeType.INCREASE_ATTACK_AND_HEALTH_DEPENDS_ON_TOKENS:
                    logger.debug ('eptitude.type: INCREASE_ATTACK_AND_HEALTH_DEPENDS_ON_TOKENS')
                    self.increase_a_h_depepend_on_tokens(targets, eptitude)

                if eptitude.type == EptitudeType.UNIT_FROM_DECK:
                    logger.debug ('eptitude.type: UNIT_FROM_DECK')
                    self.unit_from_deck(eptitude)

                if eptitude.type == EptitudeType.UNIT_COPY_FROM_DECK:
                    logger.debug ('eptitude.type: UNIT_COPY_FROM_DECK')
                    self.unit_copy_from_deck(targets, eptitude)

                if eptitude.type == EptitudeType.INCREASE_CARD_PRICE:
                    logger.debug ('eptitude.type: INCREASE_CARD_PRICE')
                    self.increase_card_price(self.unit, targets, eptitude)

                if eptitude.type == EptitudeType.DECREASE_CARD_PRICE:
                    logger.debug ('eptitude.type: DECREASE_CARD_PRICE')
                    self.decrease_card_price(self.unit, targets, eptitude)

                if eptitude.type == EptitudeType.INCREASE_CARD_PRICE_MIXIN:
                    logger.debug ('eptitude.type: INCREASE_CARD_PRICE_MIXIN')
                    self.increase_card_price_mixin(self.unit, targets, eptitude)

                if eptitude.type == EptitudeType.DECREASE_CARD_PRICE_MIXIN:
                    logger.debug ('eptitude.type: DECREASE_CARD_PRICE_MIXIN')
                    self.decrease_card_price_mixin(self.unit, targets, eptitude)

                if eptitude.type == EptitudeType.INCREASE_HEALTH_DEPENDS_ON_ASSOCIATE_CARDS:
                    logger.debug ('eptitude.type: INCREASE_HEALTH_DEPENDS_ON_ASSOCIATE_CARDS')
                    self.increase_health_depends_on_associate_cards(targets, eptitude)

                if eptitude.type == EptitudeType.INCREASE_HEALTH_DEPENDS_ON_OPPONENT_CARDS:
                    logger.debug ('eptitude.type: INCREASE_HEALTH_DEPENDS_ON_OPPONENT_CARDS')
                    self.increase_health_depends_on_opponent_cards(targets, eptitude)

                if eptitude.type == EptitudeType.REPLACE_CARD_AND_TOKEN:
                    logger.debug ('eptitude.type: REPLACE_CARD_AND_TOKEN')
                    self.replace_card_and_token(targets, eptitude)

                if eptitude.type == EptitudeType.UNIT_FROM_HAND:
                    logger.debug ('eptitude.type: UNIT_FROM_HAND')
                    self.unit_from_hand(targets, eptitude)

                if eptitude.type == EptitudeType.SHIELD_PROVOCATION_OR_DOUBLE_ATTACK:
                    logger.debug ('eptitude.type: SHIELD_PROVOCATION_OR_DOUBLE_ATTACK')
                    self.shield_provocation_or_doubleAttack(targets)

                if eptitude.type == EptitudeType.CHANGE_UNIT_TO_RANDOM_FOR_SAME_PRICE:
                    logger.debug ('eptitude.type: CHANGE_UNIT_TO_RANDOM_FOR_SAME_PRICE')
                    self.change_unit_to_random_for_same_price(targets)

                if eptitude.type == EptitudeType.OVERLOAD:
                    logger.debug ('eptitude.type: OVERLOAD')
                    self.overload (targets, eptitude)

                if eptitude.type == EptitudeType.DROP_CARD:
                    logger.debug('eptitude.type: DROP_CARD')
                    self.dropCard(targets, eptitude)

                if eptitude.type == EptitudeType.SELECT_GUISE:
                    logger.debug('eptitude.type: SELECT_GUISE')
                    self.selectGuise(targets, eptitude)


                if eptitude.type == EptitudeType.ATTACK_RANDOM_UNIT:
                    logger.debug('eptitude.type: ATTACK_RANDOM_UNIT')
                    if self.unit.whiteFlag:
                        opponentRow = self.match.blackUnitRow
                        opponentHero = self.match.blackHeroUnit
                    else:
                        opponentRow = self.match.whiteUnitRow
                        opponentHero = self.match.whiteHeroUnit
                    list = []
                    for item in opponentRow:
                        if item == self.match.targetUnit:
                            pass
                        else:
                            list.append(item)

                    if self.match.targetUnit == opponentHero:
                        pass
                    else:
                        list.append(opponentHero)

                    if len(list) > 0:
                        index = random.randint (0, len(list)-1)
                        self.match.targetUnit = list[index]

                    if len(list) > 1:
                        #TODO and here we should add activate animation action with self.unit to scenario
                        targetAttachment = self.match.initAttachment (self.unit, self.whiteFlag)
                        targetIndex = self.match.initIndex (self.unit, targetAttachment, self.whiteFlag)
                        action = {}
                        action['type'] = Action.ACTIVATE_WIDGET
                        action['client'] = self.client
                        action['targetIndex'] = targetIndex
                        action['targetAttachment'] = targetAttachment
                        self.scenario.append(action)

                if eptitude.type == EptitudeType.PRIMARY_TARGET:
                    logger.debug('eptitude.type: PRIMARY_TARGET')
                    activateFlag = False
                    try:
                        raceId = eptitude.race
                        Race.objects.get(id=raceId)
                        raceFlag = True
                    except:
                        raceFlag = False

                    logger.debug('raceFlag:%s' % (raceFlag))

                    if raceFlag:
                          try:
                               logger.debug('attackUnit.race.id:%s , raceId:%s' % (self.match.attackUnit.race.id, raceId))
                               if self.match.attackUnit.race.id == raceId:
                                    self.match.targetUnit = self.unit
                                    activateFlag = True
                          except:
                                pass
                    else:
                          self.match.targetUnit = self.unit
                          activateFlag = True

                    if activateFlag:
                        targetAttachment = self.match.initAttachment (self.unit, self.whiteFlag)
                        targetIndex = self.match.initIndex (self.unit, targetAttachment, self.whiteFlag)
                        action = {}
                        action['type'] = Action.ACTIVATE_WIDGET
                        action['client'] = self.client
                        action['targetIndex'] = targetIndex
                        action['targetAttachment'] = targetAttachment
                        self.scenario.append(action)

                if eptitude.type == EptitudeType.INCREASE_MANA:
                    self.increaseMana(targets, eptitude)

                if eptitude.type == EptitudeType.DECREASE_MANA:
                    self.decreaseMana(targets, eptitude)

                if eptitude.type == EptitudeType.ATTACH_EPTITUDE:
                    logger.debug ('eptitude.type: ATTACH_EPTITUDE')
                    self.attach_eptitude (targets, eptitude)

                if eptitude.type == EptitudeType.COPY_CARD_FROM_HAND:
                    logger.debug ('eptitude.type: COPY_CARD_FROM_HAND')
                    self.copyCardFromHand (targets, eptitude)

                if eptitude.type == EptitudeType.COPY_CARD_FROM_DECK:
                    logger.debug ('eptitude.type: COPY_CARD_FROM_DECK')
                    self.copyCardFromDeck (targets, eptitude)

                if eptitude.type == EptitudeType.DESTROY_SHADOW:
                    logger.debug ('eptitude.type: DESTROY_SHADOW')
                    self.destroy_shadow (targets)

                if eptitude.type == EptitudeType.MULTIPLY_HEALTH:
                    logger.debug ('eptitude.type: MULTYPLY_HEALTH')
                    self.multiplyHealth (targets, eptitude)

                if eptitude.type == EptitudeType.GENERATE_UNIT_CARD:
                    logger.debug ('eptitude.type: GENERATE_UNIT_CARD')
                    self.generateCard (targets, eptitude, CardType.UNIT)

                if eptitude.type == EptitudeType.GENERATE_SPELL_CARD:
                    logger.debug ('eptitude.type: GENERATE_SPELL_CARD')
                    self.generateCard (targets, eptitude, CardType.SPELL)

                if eptitude.type == EptitudeType.SHUFFLE_UNIT_TO_DECK:
                    logger.debug ('eptitude.type: SHUFFLE_UNIT_TO_DECK')
                    self.shuffleUnitToDeck (targets, eptitude)

                if eptitude.type == EptitudeType.COPY_UNIT_CARDS_TO_HAND:
                    logger.debug ('eptitude.type: COPY_UNIT_CARDS_TO_HAND')
                    self.copyUnitCardsToHand (targets, eptitude)

                if eptitude.type == EptitudeType.DESTROY_PROVOCATION:
                    logger.debug ('eptitude.type: DESTOY_PROVOCATION')
                    self.destroyProvocation (targets, eptitude)

                if eptitude.type == EptitudeType.TAKE_UP_WEAPON:
                    logger.debug ('eptitude.type: TAKE_UP_WEAPON')
                    self.takeUpWeapon(targets, eptitude)

                if eptitude.type == EptitudeType.CARD_FROM_GRAVEYARD:
                    logger.debug ('eptitude.type: CARD_FROM_GRAVEYARD')
                    self.cardFromGraveYard(targets, eptitude)

                if eptitude.type == EptitudeType.MINION_FROM_GRAVEYARD:
                    logger.debug ('eptitude.type: MINION_FROM_GRAVEYARD')
                    self.minionFromGraveYard(targets, eptitude)

                if eptitude.manacost > 0:
                     logger.debug('Eptitude manacost: %s' % eptitude.manacost)
                     self.decreaseManacost (eptitude.manacost)

                if eptitude.lifecycle > 0:
                    logger.debug ('eptitude.lifecycle > 0')
                    for target in targets:
                        target.tempEptitudes.append (eptitude.clone())

                if eptitude.period == EptitudePeriod.ACTIVATE_ACTIVE:
                    self.blockActive()

                if eptitude.widget > 0:
                    self.attachWidget(targets, eptitude.widget)

                if eptitude.activated and eptitude.destroy:
                    self.unit.destroyEptitude(eptitude)

            self.activate(period)

    def takeUpWeapon (self, targets, eptitude):
        if self.whiteFlag:
            playerHero = self.match.whiteHeroUnit
            opponentHero = self.match.blackHeroUnit
        else:
            playerHero = self.match.blackHeroUnit
            opponentHero =  self.match.whiteHeroUnit

        #try:
        weaponId = eptitude.weapon
        weapon = Weapon.objects.get(id=weaponId)

        playerWeaponIndex = 0
        opponentWeaponIndex = 0

        if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
            logger.debug ('associate')
            playerWeaponIndex =  playerHero.takeUpWeapon(weapon)
        elif eptitude.attachment == EptitudeAttachment.OPPONENT:
            logger.debug ('opponent')
            opponentWeaponIndex = opponentHero.takeUpWeapon(weapon)
        else:
            logger.debug ('all')
            playerWeaponIndex = playerHero.takeUpWeapon(weapon)
            opponentWeaponIndex = opponentHero.takeUpWeapon(weapon)

        action = {}
        action['type'] = Action.TAKE_UP_WEAPON
        action['client'] = self.client
        action['playerWeaponIndex'] = playerWeaponIndex
        action['opponentWeaponIndex'] = opponentWeaponIndex
        action['weaponId'] = weaponId
        action['power'] = weapon.power
        action['strength'] = weapon.strength
        self.scenario.append (action)


        #except:
        #    logger.debug('no_weapon_init')
        #    pass



    def decreaseHealth (self, targets, eptitude):
        if len(targets):
            eptitude.activated = True
        else:
             return

        power = eptitude.power

        for target in targets:

            target.maxHealth = target.maxHealth - power
            if target.health > target.maxHealth:
                target.health = target.maxHealth

            action = {}
            action['type'] = Action.DECREASE_HEALTH
            action['client'] = self.client
            targetAttachment = self.match.initAttachment (target, self.whiteFlag)
            targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
            action['index'] = targetIndex
            action['attachment'] = targetAttachment
            action['health'] = target.health
            action['maxHealth'] = target.maxHealth
            self.scenario.append (action)

            if target.maxHealth == 0:
                action = {}
                action['type'] = Action.DAMAGE
                action['client'] = self.client
                action['targets'] = [{'index':targetIndex, 'attachment':targetAttachment, 'damage':power}]
                self.scenario.append(action)

                self.match.deleteUnit (targetIndex, targetAttachment, self.whiteFlag)
                action = {}
                action['type'] = Action.TOKEN_DEATH
                action['client'] = self.client
                action['targetIndex'] = targetIndex
                action['targetAttachment'] = targetAttachment
                self.scenario.append(action)



    def destroyProvocation (self, targets, eptitude):
        if len(targets):
            eptitude.activated = True
        else:
             return

        for target in targets:
             target.provocation = False
             action = {}
             action['type'] = Action.DESTROY_PROVOCATION
             action['client'] = self.client
             targetAttachment = self.match.initAttachment (target, self.whiteFlag)
             targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
             action['index'] = targetIndex
             action['attachment'] = targetAttachment
             self.scenario.append (action)


    def attachWidget(self, targets, widget):
         if not len(targets):
             return

         for target in targets:
             action = {}
             action['type'] = Action.ATTACH_WIDGET
             action['client'] = self.client
             targetAttachment = self.match.initAttachment (target, self.whiteFlag)
             targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
             action['index'] = targetIndex
             action['attachment'] = targetAttachment
             action['widget'] = widget
             self.scenario.append (action)



    def blockActive(self):
        self.match.blockActive(self.unit, self.whiteFlag)

    def decreaseManacost (self, manacost):
        self.match.decreaseManacost(manacost, self.whiteFlag)

    def shuffleUnitToDeck(self, targets, eptitude):

        if len(targets):
            eptitude.activated = True
        else:
             return

        units = []
        for target in targets:
            targetAttachment = self.match.initAttachment (target, self.whiteFlag)
            targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
            if target.whiteFlag:
                targetHand = self.match.white_hand
            else:
                targetHand = self.match.black_hand
            card = self.match.getCardById(target.cardData['id'])
            cardData = self.match.getUnitCardData(card)
            cardData['whiteFlag'] = target.whiteFlag
            units.append({'index':targetIndex,'attachment':targetAttachment, 'card':cardData})
            index = random.randint(0, len(targetHand) - 1)
            targetHand.insert(index,cardData)

        action = {}
        action['type'] = Action.SHUFFLE_UNIT_TO_DECK
        action['targets'] = units
        action['client'] = self.client
        self.scenario.append (action)

        for target in targets:
            try:
                index = self.match.whiteUnitRow.index(target)
                del self.match.whiteUnitRow[index]
            except:
                try:
                   index = self.match.blackUnitRow.index(target)
                   del self.match.blackUnitRow[index]
                except:
                    pass

        for target in targets:
            if self.containsDynamicEptitudes (target):
                self.deactivateDynamic (target)


    def fly(self, targets, eptitude):
        if len(targets):
            eptitude.activated = True
        else:
             return

        for target in targets:
            target.fly = True
            action = {}
            action['type'] = Action.FLY
            action['client'] = self.client
            targetAttachment = self.match.initAttachment (target, self.whiteFlag)
            targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
            action['index'] = targetIndex
            action['attachment'] = targetAttachment
            self.scenario.append (action)


    def multiplyAttack(self, targets, eptitude):
        if len(targets):
            eptitude.activated = True
        else:
             return

        for target in targets:
            target.setAttack(target.getAttack() * 2)
            action = {}
            action['type'] = Action.INCREASE_ATTACK
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action["attack"] = target.getAttack()
            targetAttachment = self.match.initAttachment (target, self.whiteFlag)
            targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
            action['index'] = targetIndex
            action['attachment'] = targetAttachment
            self.scenario.append (action)

    def multiplyHealth(self, targets, eptitude):
        if len(targets):
            eptitude.activated = True
        else:
             return

        for target in targets:
            target.setHealth(target.getHealth() * 2)
            if target.getHealth() > target.getMaxHealth():
                target.setMaxHealth (target.getHealth())
            action = {}
            action['type'] = Action.CHANGE_HEALTH
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action["health"] = target.getHealth()
            action['maxHealth'] = target.getMaxHealth()
            targetAttachment = self.match.initAttachment (target, self.whiteFlag)
            targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
            action['index'] = targetIndex
            action['attachment'] = targetAttachment
            self.scenario.append (action)



    def selectGuise(self, targets, eptitude):
        if len(targets):
            eptitude.activated = True
        else:
             return

        groupId = eptitude.group
        group = Group.objects.get(pk=groupId)
        cards = []

        for selectCard in group.cards:
                selectCardData = self.match.getUnitCardData (selectCard)
                selectCardData['whiteFlag'] = self.whiteFlag
                cards.append(selectCardData)

        self.match.guiseCards = cards

        action = {}
        action['type'] = Action.SELECT_GUISE
        action['client'] = self.client
        action['cards'] = cards
        self.scenario.append (action)

        logger.debug(cards)

    def dropCard (self, targets, eptitude):
        if len(targets):
            eptitude.activated = True
        else:
             return

        if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
            if self.whiteFlag:
                targetHand = self.match.white_hand
            else:
                targetHand = self.match.black_hand

        if eptitude.attachment == EptitudeAttachment.OPPONENT:
            if self.whiteFlag:
                targetHand = self.match.black_hand
            else:
                targetHand = self.match.black_hand

        count = eptitude.power

        cardDatas = []
        cards = []
        indexes = []

        if not len(targetHand):
           return

        for i in range(count):
            if len(indexes) < len(targetHand):
                index = self.getFreeIndex(targetHand, indexes)
                logger.debug('dropCard.index:%s' % index)
                card = targetHand[index]
                attachment, index = self.match.initCardAttachment(card, self.whiteFlag)
                cardData = {}
                cardData['card'] = card
                cardData['index'] = index
                cardDatas.append(cardData)
                cards.append(card)

        logger.debug('cardDatas.length:%s' % len(cardDatas))

        for card in cards:
            attachment, index = self.match.initCardAttachment(card, self.whiteFlag)
            del targetHand[index]

        if len(cards):
            action = {}
            action['type'] = Action.DROP_CARDS
            action['client'] = self.client
            # TODO разсинхрон, нужно исправить!
            if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
                action['attachment'] = 1
            else:
                action['attachment'] = 0
            action['cards'] = cardDatas
            action['endAnimationFlag'] = True
            self.scenario.append(action)

    def getFreeIndex(self, hand, indexes):
        index = random.randint(0, len(hand) - 1)
        try:
            indexes.index(index)
            index = self.getFreeIndex(hand, indexes)
            return index
        except:
            indexes.append(index)
            return index

    def generateCard(self, targets, eptitude, type):
        if len(targets):
            eptitude.activated = True
        else:
             return

        if self.whiteFlag:
            playerHand = self.match.white_hand
            opponentHand = self.match.black_hand
            row = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
        else:
            playerHand = self.match.black_hand
            opponentHand = self.match.black_hand
            row = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow

        try:
            card = Card.objects.get(id=eptitude.unit)
        except:
            cards = Card.objects.filter(auxiliary=False,type=type)
            index = random.randint(0, len(cards) - 1)
            card = cards[index]

        cardData = self.match.getUnitCardData(card)

        if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
            playerHand.append(cardData)
            cardData['whiteFlag'] = self.whiteFlag

        if eptitude.attachment == EptitudeAttachment.OPPONENT:
            opponentHand.append(cardData)
            cardData['whiteFlag'] = not self.whiteFlag

        self.match.configureLastCard(cardData)

        action = {}
        action['type'] = Action.CARD
        action['client'] = self.client
        action['attachment'] = eptitude.attachment
        action['card'] = cardData
        action['endAnimationFlag'] = True
        self.scenario.append(action)

        for unit in row:
            controller = Controller()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.newCard(unit)
            if cardData['whiteFlag'] == unit.whiteFlag:
                controller.newPlayerCard(unit)
            else:
                controller.newOpponentCard(unit)

        for unit in opponentRow:
            controller = Controller()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.newCard(unit)
            if cardData['whiteFlag'] == unit.whiteFlag:
                controller.newPlayerCard(unit)
            else:
                controller.newOpponentCard(unit)

        controller = CardController()
        controller.setWhiteFlag(self.whiteFlag)
        controller.setMatch(self.match)
        controller.setScenario(self.scenario)
        controller.setClient(self.client)
        controller.new_card()


    def copyCardFromHand (self, targets, eptitude):
        if len(targets):
            eptitude.activated = True
        else:
             return

        if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
            if self.whiteFlag:
                targetHand = self.match.white_hand
            else:
                targetHand = self.match.black_hand

        if eptitude.attachment == EptitudeAttachment.OPPONENT:
            if self.whiteFlag:
                targetHand = self.match.black_hand
            else:
                targetHand = self.match.white_hand

        if self.whiteFlag:
            playerHand = self.match.white_hand
            row = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
        else:
            playerHand = self.match.black_hand
            row = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow

        count = eptitude.power

        if not len(targetHand):
            return

        for i in range(count):

            if len (playerHand) == 10:
                return

            index = random.randint(0, len(targetHand) - 1)
            card = targetHand[index]
            copy = self.match.copyCard(card)
            playerHand.append(copy)
            self.match.configureLastCard(copy)
            copy['whiteFlag'] = self.whiteFlag

            action = {}
            action['type'] = Action.CARD
            action['client'] = self.client
            action['attachment'] = EptitudeAttachment.ASSOCIATE
            action['card'] = copy
            action['endAnimationFlag'] = True
            self.scenario.append(action)

        for unit in row:
            controller = Controller()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.newCard(unit)
            if card['whiteFlag'] == unit.whiteFlag:
                controller.newPlayerCard(unit)
            else:
                controller.newOpponentCard(unit)

        for unit in opponentRow:
            controller = Controller()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.newCard(unit)
            if card['whiteFlag'] == unit.whiteFlag:
                controller.newPlayerCard(unit)
            else:
                controller.newOpponentCard(unit)

        controller = CardController()
        controller.setWhiteFlag(self.whiteFlag)
        controller.setMatch(self.match)
        controller.setScenario(self.scenario)
        controller.setClient(self.client)
        controller.new_card()


    def copyCardFromDeck (self, targets, eptitude):

        if len(targets):
            eptitude.activated = True
        else:
             return

        if self.whiteFlag:
            playerDeck = self.match.white_match_deck
            opponentDeck = self.match.black_match_deck
            playerHand = self.match.white_hand
            row = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
        else:
            playerDeck = self.match.black_match_deck
            opponentDeck = self.match.white_match_deck
            playerHand = self.match.black_hand
            row = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow

        if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
            deck = playerDeck
        elif eptitude.attachment == EptitudeAttachment.OPPONENT:
            deck = opponentDeck
        else:
            return

        count = eptitude.power

        iteration = 0

        for i in range(count):
            # if deck is empty
            if not len(deck):
                return
            # if deck is shorter than eptitude power
            if len(deck) == iteration:
                return
            iteration += 1

            index = random.randint(0, len(deck) - 1)
            card = deck[index]
            copy = self.match.copyCard(card)
            playerHand.append(copy)
            self.match.configureLastCard(copy)
            copy['whiteFlag'] = self.whiteFlag

            action = {}
            action['type'] = Action.CARD
            action['client'] = self.client
            action['attachment'] = EptitudeAttachment.ASSOCIATE
            action['card'] = copy
            action['endAnimationFlag'] = True
            self.scenario.append(action)

            for unit in row:
                controller = Controller()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.newCard(unit)
                if copy['whiteFlag'] == unit.whiteFlag:
                    controller.newPlayerCard(unit)
                else:
                    controller.newOpponentCard(unit)

            for unit in opponentRow:
                controller = Controller()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.newCard(unit)
                if copy['whiteFlag'] == unit.whiteFlag:
                    controller.newPlayerCard(unit)
                else:
                    controller.newOpponentCard(unit)

            controller = CardController()
            controller.setWhiteFlag(self.whiteFlag)
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.new_card()

    def overload (self, targets, eptitude):
        if len(targets):
            eptitude.activated = True
        else:
             return

        whiteOverload = False
        blackOverload = False
        playerPrice = False
        opponentPrice = False

        if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
            if self.whiteFlag:
                whiteOverload = True
                playerPrice = self.match.white_price + 1
            else:
                blackOverload = True
                playerPrice = self.match.black_price + 1

        elif eptitude.attachment == EptitudeAttachment.OPPONENT:
            if self.whiteFlag:
                blackOverload = True
                opponentPrice = self.match.black_price + 1
            else:
                whiteOverload = True
                opponentPrice = self.match.white_price + 1


        else:
            whiteOverload = True
            blackOverload = True
            if self.whiteFlag:
                 playerPrice = self.match.white_price + 1
                 opponentPrice = self.match.black_price + 1
            else:
                 playerPrice = self.match.black_price + 1
                 opponentPrice = self.match.white_price + 1

        if whiteOverload:
            self.match.whiteOverload += eptitude.power

        if blackOverload:
            self.match.blackOverload += eptitude.power

        if self.whiteFlag:
            playerOverload = self.match.whiteOverload
            opponentOverload = self.match.blackOverload
        else:
            opponentOverload = self.match.whiteOverload
            playerOverload = self.match.blackOverload

        action = {}
        action['type'] = Action.OVERLOAD
        action['client'] = self.client
        if playerPrice:
            action['playerPrice'] = playerPrice
        if opponentPrice:
            action['opponentPrice'] = opponentPrice
        action['playerOverload'] = playerOverload
        action['opponentOverload'] = opponentOverload
        action['endAnimationFlag'] = True
        action['attachment'] = eptitude.attachment
        self.scenario.append (action)




    def attach_eptitude (self, targets, eptitude):
         logger.debug ('attach_apptitude')
         logger.debug ('len.targets:%s' % len(targets))
         if len(targets):
             eptitude.activated = True
         else:
             return

         logger.debug('attach_eptitude.id: %s' % eptitude.attach_eptitude)
         attachedEptitude = self.unit.getEptitudeById(eptitude.attach_eptitude)
         logger.debug(attachedEptitude)
         for target in targets:
             cloneEptitude = attachedEptitude.clone()
             cloneEptitude.attached = True
             target.attachEptitude(cloneEptitude)
             controller = Controller()
             controller.setMatch(self.match)
             controller.setScenario(self.scenario)
             controller.setClient(self.client)
             controller.setWhiteFlag(self.whiteFlag)
             controller.activateEptitude(target)



    def destroy_shadow (self, targets):
           for target in targets:
               action = {}
               target.shadow = False
               action['type'] = Action.DESTROY_SHADOW
               action['client'] = self.client
               targetAttachment = self.match.initAttachment (target, self.whiteFlag)
               targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
               action['index'] = targetIndex
               action['attachment'] = targetAttachment
               action['endAnimationFlag'] = False
               self.scenario.append (action)

    def change_health_till(self, targets, eptitude):
        power = eptitude.power
        for target in targets:
            target.setMaxHealth(power)
            target.setHealth(power)
            action = {}
            action['type'] = Action.CHANGE_HEALTH
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action["health"] = target.getHealth()
            action["maxHealth"] = target.getMaxHealth()
            targetAttachment = self.match.initAttachment (target, self.whiteFlag)
            targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
            action['index'] = targetIndex
            action['attachment'] = targetAttachment
            self.scenario.append (action)

    def full_health (self, targets, eptitude):
        if len(targets):
            eptitude.activated = True

        for target in targets:
            target.setHealth(target.getMaxHealth())
            action = {}
            action['type'] = Action.CHANGE_HEALTH
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action["health"] = target.getHealth()
            action["maxHealth"] = target.getMaxHealth()
            targetAttachment = self.match.initAttachment (target, self.whiteFlag)
            targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
            action['index'] = targetIndex
            action['attachment'] = targetAttachment
            self.scenario.append (action)

    def spellInvisible (self, targets):
        for target in targets:
            target.spellInvisible = True

            targetAttachment = self.match.initAttachment (target, self.whiteFlag)
            targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)

            action = {}
            action['type'] = Action.SPELL_INVISIBLE
            action['client'] = self.client
            action['targetIndex'] = targetIndex
            action['targetAttachment'] = targetAttachment
            self.scenario.append(action)


    def increaseSpell (self, targets, eptitude):
         for target in targets:
            target.spellUp = True

            if target.whiteFlag:
                spellMixin = self.match.whiteSpellMixin + eptitude.power
                self.match.whiteSpellMixin = spellMixin
                client = self.match.getWhiteId()
            else:
                spellMixin = self.match.blackSpellMixin + eptitude.power
                self.match.blackSpellMixin = spellMixin
                client = self.match.getBlackId()

            targetAttachment = self.match.initAttachment (target, self.whiteFlag)
            targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)

            action = {}
            action['type'] = Action.INCREASE_SPELL
            action['client'] = self.client
            action['spellClient'] = client
            action['endAnimationFlag'] = True
            action['targetIndex'] = targetIndex
            action['targetAttachment'] = targetAttachment
            action['spellMixin'] = spellMixin
            self.scenario.append(action)

    def decreaseSpell (self, targets, eptitude):
         logger.debug ('spellTargets length:%s' % len(targets))
         for target in targets:
            target.spellUp = False
            if target.whiteFlag:
                spellMixin = self.match.whiteSpellMixin - eptitude.power
                self.match.whiteSpellMixin = spellMixin
                client = self.match.getWhiteId()
            else:
                spellMixin = self.match.blackSpellMixin - eptitude.power
                self.match.blackSpellMixin = spellMixin
                client = self.match.getBlackId()

            targetAttachment = self.match.initAttachment (target, self.whiteFlag)
            targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)

            action = {}
            action['type'] = Action.DECREASE_SPELL
            action['client'] = self.client
            action['spellClient'] = client
            action['endAnimationFlag'] = True
            action['targetIndex'] = targetIndex
            action['targetAttachment'] = targetAttachment
            action['spellMixin'] = spellMixin
            self.scenario.append(action)



    def change_unit_to_random_for_same_price(self, targets):
        for target in targets:
            price = target.cardData['price']
            unitCard = random.choice(Card.objects.filter(price=price))
            cardData = self.match.getUnitCardData(unitCard)
            targetUnit = Unit(cardData)
            targetUnit.setWhiteFlag(target.whiteFlag)

            targetAttachment = self.match.initAttachment (target, self.whiteFlag)
            targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)

            if target.whiteFlag:
                row = self.match.whiteUnitRow
            else:
                row = self.match.blackUnitRow

            self.match.deleteUnit (targetIndex, targetAttachment, self.whiteFlag)
            row.insert(targetIndex, targetUnit)

            action = {}
            action['type'] = Action.CHANGE_UNIT
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['targetIndex'] = targetIndex
            action['targetAttachment'] = targetAttachment
            action['cardData'] = targetUnit.cardData
            action['attack'] = targetUnit.attack
            action['health'] = targetUnit.health
            self.scenario.append(action)

            self.addUnit(targetUnit)
            self.unitPlaced (targetUnit)





    def copy_unit(self, targets, eptitude):
        for target in targets:
            targetUnit = Unit(target.cardData)
            targetUnit.setWhiteFlag(self.unit.whiteFlag)

            targetAttachment = self.match.initAttachment (self.unit, self.whiteFlag)
            targetIndex = self.match.initIndex (self.unit, targetAttachment, self.whiteFlag)

            if self.unit.whiteFlag:
                row = self.match.whiteUnitRow
            else:
                row = self.match.blackUnitRow

            self.match.deleteUnit (targetIndex, targetAttachment, self.whiteFlag)
            row.insert(targetIndex, targetUnit)

            targetUnit.provocation = target.provocation
            targetUnit.doubleAttack = target.doubleAttack
            targetUnit.attackCount = target.attackCount
            targetUnit.jerk = target.jerk
            targetUnit.canAttack = target.canAttack
            targetUnit.shadow = target.shadow
            targetUnit.freeze = target.freeze
            targetUnit.freezeIndex = target.freezeIndex
            targetUnit.dumbness = target.dumbness
            targetUnit.attack = target.attack
            targetUnit.health = target.health
            targetUnit.shield = target.shield
            targetUnit.spellInvisible = target.spellInvisible
            targetUnit.spellUp = target.spellUp

            targetUnit.destroyBattlecryEptitudes()

            action = {}
            action['type'] = Action.CHANGE_UNIT
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['targetIndex'] = targetIndex
            action['targetAttachment'] = targetAttachment
            action['cardData'] = targetUnit.cardData
            action['provocation'] = targetUnit.provocation
            action['doubleAttack'] = targetUnit.doubleAttack
            action['attackCount'] = targetUnit.attackCount
            action['jerk'] = targetUnit.jerk
            action['canAttack'] = targetUnit.canAttack
            action['shadow'] =targetUnit.shadow
            action['freeze'] = targetUnit.freeze
            action['freezeIndex'] = targetUnit.freezeIndex
            action['dumbness'] = targetUnit.dumbness
            action['attack'] = targetUnit.attack
            action['health'] = targetUnit.health
            action['shield'] = targetUnit.shield
            action['spellInvisible'] = target.spellInvisible
            action['spellUp'] = target.spellUp
            self.scenario.append(action)

            if self.containsDynamicEptitudes(targetUnit):
                self.activateDynamic(targetUnit)

            controller = Controller()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.addUnit(targetUnit)

            controller = Controller()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.unitPlaced (targetUnit)

            controller = CardController()
            controller.setWhiteFlag(self.whiteFlag)
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.new_unit()

    def unit_convertion(self, targets, eptitude):
        for target in targets:
            #targetUnit = Unit(target.cardData)
            #targetUnit.setWhiteFlag(self.unit.whiteFlag)

            targetAttachment = self.match.initAttachment (target, self.whiteFlag)
            targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)

            if self.unit.whiteFlag:
                row = self.match.whiteUnitRow
                opponentRow = self.match.blackUnitRow
            else:
                row = self.match.blackUnitRow
                opponentRow = self.match.whiteUnitRow

            self.match.deleteUnit (targetIndex, targetAttachment, self.whiteFlag)

            card = Card.objects.get(id=eptitude.unit)
            cardData = self.match.getUnitCardData(card)
            convertionUnit =  Unit(cardData)

            controller =  Controller()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(target.whiteFlag)
            controller.configureUnit (convertionUnit)

            if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
                row.insert(targetIndex, convertionUnit)
                convertionUnit.setWhiteFlag(self.whiteFlag)
            else:
                opponentRow.insert(targetIndex, convertionUnit)
                convertionUnit.setWhiteFlag(not self.whiteFlag)

            action = {}
            action['type'] = Action.CHANGE_UNIT
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['targetIndex'] = targetIndex
            action['targetAttachment'] = targetAttachment
            action['cardData'] = convertionUnit.cardData
            action['provocation'] = convertionUnit.provocation
            action['doubleAttack'] = convertionUnit.doubleAttack
            action['attackCount'] = convertionUnit.attackCount
            action['jerk'] = convertionUnit.jerk
            action['canAttack'] = convertionUnit.canAttack
            action['shadow'] = convertionUnit.shadow
            action['freeze'] = convertionUnit.freeze
            action['freezeIndex'] = convertionUnit.freezeIndex
            action['dumbness'] = convertionUnit.dumbness
            action['attack'] = convertionUnit.attack
            action['health'] = convertionUnit.health
            action['shield'] = convertionUnit.shield
            action['spellInvisible'] = convertionUnit.spellInvisible
            action['spellUp'] = convertionUnit.spellUp
            self.scenario.append(action)

            if self.containsDynamicEptitudes(convertionUnit):
                self.activateDynamic(convertionUnit)



    def entice_unit(self, targets, eptitude):
        for target in targets:

            if target.whiteFlag:
                row = self.match.whiteUnitRow
                opponentRow = self.match.blackUnitRow
                opponentFlag = False
            else:
                row = self.match.blackUnitRow
                opponentRow = self.match.whiteUnitRow
                opponentFlag = True

            if len(opponentRow) < 7:
                if self.containsDynamicEptitudes (target):
                    self.deactivateDynamic (target)

                eptitude.target = target

                targetAttachment = self.match.initAttachment (target, self.whiteFlag)
                targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)

                self.match.deleteUnit (targetIndex, targetAttachment, self.whiteFlag)

                target.setWhiteFlag(opponentFlag)
                opponentIndex = len(opponentRow)

                # добавляем в ряд
                target.setRow(opponentRow)
                target.setIndex(opponentIndex)
                opponentRow.insert (opponentIndex, target)

                action = {}
                action['type'] = Action.ENTICE_UNIT
                action['client'] = self.client
                action['endAnimationFlag'] = True
                action['targetIndex'] = targetIndex
                action['targetAttachment'] = targetAttachment
                self.scenario.append(action)

                for unit in row:
                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.enticeAssociate(unit)

                for unit in opponentRow:
                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.enticeOpponent(unit)

                if self.containsDynamicEptitudes (target):
                    self.activateDynamic (target)







    def changeExtraAttackTill(self, targets, eptitude):
        power = eptitude.power
        for target in targets:
            target.extraAttack = power
            action = {}
            action['type'] = Action.INCREASE_ATTACK
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action["attack"] = target.getTotalAttack()
            targetAttachment = self.match.initAttachment (target, self.whiteFlag)
            targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
            action['index'] = targetIndex
            action['attachment'] = targetAttachment
            self.scenario.append (action)

    def attack_equals_to_health (self, targets, eptitude):
         if len(targets):
             eptitude.activated = True
         else:
             return

         for target in targets:

            target.attack = target.getHealth()
            action = {}
            action['type'] = Action.INCREASE_ATTACK
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action["attack"] = target.getTotalAttack()
            targetAttachment = self.match.initAttachment (target, self.whiteFlag)
            targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
            action['index'] = targetIndex
            action['attachment'] = targetAttachment
            self.scenario.append (action)

            if target.getAttack() > 0:
                target.canAttack = True

            if target.whiteFlag == self.whiteFlag and target.attackCount > 0 and target.stepCount > 0 and target.canAttack:
                 action = {}
                 action['type'] = Action.ATTACK_AVAILABLE
                 action['client'] = self.client
                 action['endAnimationFlag'] = False
                 da_units = []
                 da_units.append (target.row.index(target))
                 action['unitList'] = da_units
                 self.scenario.append(action)

                 action = {}
                 action['type'] = Action.GLOW_UNITS
                 action['client'] = self.client
                 action['endAnimationFlag'] = False
                 self.scenario.append(action)

    def shield_provocation_or_doubleAttack(self, targets):
        shieldTargets = []
        provocationTargets = []
        doubleAttackTargets = []
        for target in targets:
            index = random.randint (0, 2)
            if index == 0:
                shieldTargets.append(target)
            elif index == 1:
                provocationTargets.append(target)
            else:
                doubleAttackTargets.append(target)

        self.shield(shieldTargets)
        self.provocation(provocationTargets)
        self.double_attack(doubleAttackTargets)


    def deactivateDoubleAttack(self, targets, eptitude):
        for target in targets:
             target.totalStepAttack = 1
             target.stepAttack = target.totalStepAttack - target.stepAttackCount
             if target.stepAttack < 0:
                 target.stepAttack = 0
             action = {}
             action['type'] = Action.DESTOY_DOUBLE_ATTACK
             action['client'] = self.client
             targetAttachment = self.match.initAttachment (target, self.whiteFlag)
             targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
             action['index'] = targetIndex
             action['attachment'] = targetAttachment
             action['endAnimationFlag'] = False
             self.scenario.append (action)

    def double_attack(self, targets, eptitude):
        for target in targets:
             target.totalStepAttack = eptitude.power
             target.stepAttack = target.totalStepAttack - target.stepAttackCount
             action = {}
             action['type'] = Action.DOUBLE_ATTACK
             action['client'] = self.client
             targetAttachment = self.match.initAttachment (target, self.whiteFlag)
             targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
             action['index'] = targetIndex
             action['attachment'] = targetAttachment
             action['endAnimationFlag'] = False
             self.scenario.append (action)

             if target.whiteFlag == self.whiteFlag and target.stepAttack > 0 and target.stepCount > 0:
                 action = {}
                 action['type'] = Action.ATTACK_AVAILABLE
                 action['client'] = self.client
                 action['endAnimationFlag'] = False
                 da_units = []
                 da_units.append (target.row.index(target))
                 action['unitList'] = da_units
                 self.scenario.append(action)

                 action = {}
                 action['type'] = Action.GLOW_UNITS
                 action['client'] = self.client
                 action['endAnimationFlag'] = False
                 self.scenario.append(action)


    def shield (self, targets):
         for target in targets:
             target.shield = True
             action = {}
             action['type'] = Action.SHIELD
             action['client'] = self.client
             targetAttachment = self.match.initAttachment (target, self.whiteFlag)
             targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)
             action['index'] = targetIndex
             action['attachment'] = targetAttachment
             action['endAnimationFlag'] = False
             self.scenario.append (action)

    def provocation(self, targets):
        for target in targets:
             target.provocation = True

        action = {}
        action['type'] = Action.PROVOCATION
        action['client'] = self.client
        action['endAnimationFlag'] = False
        clientTargets = self.match.getTargetsCoord(targets, self.whiteFlag)
        action["targets"] = clientTargets
        self.scenario.append (action)

    def replace_card_and_token(self, targets, eptitude):

        logger.debug ('replace card and token targets: %s' % len(targets))

        if len(targets):
            # удаляем токен со стола
            initiatorAttachment = self.match.initAttachment (self.unit, self.whiteFlag)
            initiatorIndex = self.match.initIndex (self.unit, initiatorAttachment, self.whiteFlag)
            initiatorCard = self.match.copyCard(self.unit.cardData)
            self.match.deleteUnit (initiatorIndex, initiatorAttachment, self.whiteFlag)

            card = targets[0]
            cardAttachment, cardIndex = self.match.initCardAttachment(card, self.whiteFlag)

            if self.whiteFlag:
                playerRow = self.match.whiteUnitRow
                playerHand = self.match.white_hand
            else:
                playerRow = self.match.blackUnitRow
                playerHand = self.match.black_hand

            # добавляем в ряд новую фишку соответвующую замененной карте
            targetUnit = Unit(card)
            targetUnit.whiteFlag = self.whiteFlag
            targetUnit.setRow(playerRow)
            targetUnit.replaceFlag = True
            playerRow.insert (initiatorIndex, targetUnit)

            # удаляем карту
            del playerHand[cardIndex]

            # ставим карту с инициировавшей способность фишкой в колоду
            logger.debug (initiatorCard)
            playerHand.insert(cardIndex, self.unit.cardData)

            # оповещаем клиент
            action = {}
            action['cardIndex'] = cardIndex
            action['cardAttachment'] = cardAttachment
            action['initiatorIndex'] = initiatorIndex
            action['initiatorAttachment'] = initiatorAttachment
            action['card'] = initiatorCard
            action['unit'] = targetUnit.getCardData()
            action['type'] = Action.REPLACE_CARD_AND_TOKEN
            action['client'] = self.client
            action['endAnimationFlag'] = True
            self.scenario.append (action)

    def unit_from_hand(self, targets, eptitude):
        if len(targets):
            eptitude.activated = True
        else:
            return

        if self.whiteFlag:
            hand = self.match.white_hand
            opponentHand = self.match.black_hand
            playerRow = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
        else:
            hand = self.match.black_hand
            opponentHand = self.match.white_hand
            playerRow = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow

        count = eptitude.power

        for i in range (count):
            if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
                if len(playerRow) < 7:
                    cards = self.match.getUnitCardsHandList(self.whiteFlag)
                    if len(cards):
                        index = random.randint(0, len(cards) - 1)
                        logger.debug('index:%s' % index)
                        cardData = cards[index]
                        logger.debug(cardData)
                        cardAttachment, cardIndex = self.match.initCardAttachment(cardData, self.whiteFlag)
                        del hand[cardIndex]
                        copy = self.match.copyCard(cardData)
                        targetUnit = Unit(copy)
                        targetUnit.whiteFlag = self.whiteFlag
                        targetUnit.setRow(playerRow)
                        targetIndex = len(playerRow)
                        playerRow.insert (targetIndex, targetUnit)

                        action = {}
                        action['type'] = Action.UNIT_FROM_HAND
                        action['cardIndex'] = cardIndex
                        action['cardAttachment'] = cardAttachment
                        action['initiatorIndex'] = targetIndex
                        action['initiatorAttachment'] = EptitudeAttachment.ASSOCIATE
                        action['card'] = copy
                        action['client'] = self.client
                        action['endAnimationFlag'] = True
                        self.scenario.append (action)

                        controller = Controller()
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.addUnit(targetUnit)

                        controller = Controller()
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.unitPlaced (targetUnit)

                        controller = CardController()
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.new_unit()

            if eptitude.attachment == EptitudeAttachment.OPPONENT:
                 if len(opponentRow) < 7:
                    cards = self.match.getUnitCardsHandList(not self.whiteFlag)
                    if len(cards):
                        index = random.randint(0, len(cards) - 1)
                        cardData = cards[index]
                        cardAttachment, cardIndex = self.match.initCardAttachment(cardData, self.whiteFlag)
                        del opponentHand[cardIndex]
                        copy = self.match.copyCard(cardData)
                        targetUnit = Unit(copy)
                        targetUnit.whiteFlag = not self.whiteFlag
                        targetUnit.setRow(opponentRow)
                        targetIndex = len(opponentRow)
                        opponentRow.insert (targetIndex, targetUnit)

                        action = {}
                        action['type'] = Action.UNIT_FROM_HAND
                        action['cardIndex'] = cardIndex
                        action['cardAttachment'] = cardAttachment
                        action['initiatorIndex'] = targetIndex
                        action['initiatorAttachment'] = EptitudeAttachment.OPPONENT
                        action['card'] = copy
                        action['client'] = self.client
                        action['endAnimationFlag'] = True
                        self.scenario.append (action)

                        controller = Controller()
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.addUnit(targetUnit)

                        controller = Controller()
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.unitPlaced (targetUnit)

                        controller = CardController()
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.new_unit()

            if eptitude.attachment == EptitudeAttachment.ALL:
                if len(playerRow) < 7:
                    cards = self.match.getUnitCardsHandList(self.whiteFlag)
                    if len(cards):
                        index = random.randint(0, len(cards) - 1)
                        cardData = cards[index]
                        cardAttachment, cardIndex = self.match.initCardAttachment(cardData, self.whiteFlag)
                        del hand[cardIndex]
                        copy = self.match.copyCard(cardData)
                        targetUnit = Unit(copy)
                        targetUnit.whiteFlag = self.whiteFlag
                        targetUnit.setRow(playerRow)
                        targetIndex = len(playerRow)
                        playerRow.insert (targetIndex, targetUnit)

                        action = {}
                        action['type'] = Action.UNIT_FROM_HAND
                        action['cardIndex'] = cardIndex
                        action['cardAttachment'] = cardAttachment
                        action['initiatorIndex'] = targetIndex
                        action['initiatorAttachment'] = EptitudeAttachment.ASSOCIATE
                        action['card'] = copy
                        action['client'] = self.client
                        action['endAnimationFlag'] = True
                        self.scenario.append (action)

                        targetUnit.destroyBattlecryEptitudes()

                        controller = Controller()
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.addUnit(targetUnit)

                        controller = Controller()
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.unitPlaced (targetUnit)

                        controller = CardController()
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.new_unit()

                if len(opponentRow) < 7:
                    cards = self.match.getUnitCardsHandList(not self.whiteFlag)
                    if len(cards):
                        index = random.randint(0, len(cards) - 1)
                        cardData = cards[index]
                        cardAttachment, cardIndex = self.match.initCardAttachment(cardData, self.whiteFlag)
                        del opponentHand[cardIndex]
                        copy = self.match.copyCard(cardData)
                        targetUnit = Unit(copy)
                        targetUnit.whiteFlag = not self.whiteFlag
                        targetUnit.setRow(opponentRow)
                        targetIndex = len(opponentRow)
                        opponentRow.insert (targetIndex, targetUnit)

                        action = {}
                        action['type'] = Action.UNIT_FROM_HAND
                        action['cardIndex'] = cardIndex
                        action['cardAttachment'] = cardAttachment
                        action['initiatorIndex'] = targetIndex
                        action['initiatorAttachment'] = EptitudeAttachment.OPPONENT
                        action['card'] = copy
                        action['client'] = self.client
                        action['endAnimationFlag'] = True
                        self.scenario.append (action)

                        controller = Controller()
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.addUnit(targetUnit)

                        controller = Controller()
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.unitPlaced (targetUnit)

                        controller = CardController()
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.new_unit()

    def cardFromGraveYard (self, targets, eptitude):

        if len(targets):
            eptitude.activated = True
        else:
            return

        if self.whiteFlag:
            hand = self.match.white_hand
            opponentHand = self.match.black_hand
            row = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
            graveyard = self.match.white_graveyard
            opponentGraveyard = self.match.black_graveyard

        else:
            hand = self.match.black_hand
            opponentHand = self.match.white_hand
            row = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow
            graveyard = self.match.white_graveyard
            opponentGraveyard = self.match.black_graveyard

        graveCards = []

        for i in range(eptitude.count):

            if len(hand) > 9:
                break

            # Выбираем карту cardData из нужного кладбища
            if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
                if not len(graveyard):
                    break
                index = random.randint(0, len(graveyard) - 1)
                cardData = graveyard[index]
            elif eptitude.attachment == EptitudeAttachment.OPPONENT:
                if not len(opponentGraveyard):
                    break
                index = random.randint(0, len(opponentGraveyard) - 1)
                cardData = opponentGraveyard[index]
            elif eptitude.attachment == EptitudeAttachment.ALL:
                if not len(graveyard) and not len(opponentGraveyard):
                    break
                index = random.randint(0, len(graveyard) + len(opponentGraveyard) - 1)
                if index <= len(graveyard) - 1:
                    cardData = graveyard[index]
                else:
                    index -= len(graveyard)
                    cardData = opponentGraveyard[index]

            copy = self.match.copyCard(cardData)
            copy['whiteFlag'] = self.whiteFlag
            hand.append(copy)
            graveCards.append(copy)
            self.match.lastCardinHand = copy
            self.match.configureLastCard (copy)

            for unit in row:
                controller = Controller()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.newCard(unit)
                if copy['whiteFlag'] == unit.whiteFlag:
                    controller.newPlayerCard(unit)
                else:
                    controller.newOpponentCard(unit)

            for unit in opponentRow:
                controller = Controller()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.newCard(unit)
                if copy['whiteFlag'] == unit.whiteFlag:
                    controller.newPlayerCard(unit)
                else:
                    controller.newOpponentCard(unit)

            controller = CardController()
            controller.setWhiteFlag(self.whiteFlag)
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.new_card()

        if len(graveCards):
            action = {}
            action['type'] = Action.CARDS_FROM_GRAVEYARD
            action['client'] = self.client
            action['cards'] = graveCards
            self.scenario.append (action)

        logger.debug('len graveCards: %s' % len(graveCards))

        if targets[0].whiteFlag == self.whiteFlag:
            action = {}
            action['type'] = Action.GLOW_CARDS
            action['client'] = self.client
            action['endAnimationFlag'] = False
            self.scenario.append(action)

    def minionFromGraveYard (self, targets, eptitude):
        if len(targets):
            eptitude.activated = True
        else:
            return

        if self.whiteFlag:
            hand = self.match.white_hand
            opponentHand = self.match.black_hand
            row = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
            graveyard = self.match.white_graveyard
            opponentGraveyard = self.match.black_graveyard

        else:
            hand = self.match.black_hand
            opponentHand = self.match.white_hand
            row = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow
            graveyard = self.match.white_graveyard
            opponentGraveyard = self.match.black_graveyard

        graveCards = []

        for i in range(eptitude.count):
            if len(row) >= 7:
                    break

            # Выбираем карту cardData из нужного кладбища
            if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
                if not len(graveyard):
                    break
                index = random.randint(0, len(graveyard) - 1)
                cardData = graveyard[index]
            elif eptitude.attachment == EptitudeAttachment.OPPONENT:
                if not len(opponentGraveyard):
                    break
                index = random.randint(0, len(opponentGraveyard) - 1)
                cardData = opponentGraveyard[index]
            elif eptitude.attachment == EptitudeAttachment.ALL:
                if not len(graveyard) and not len(opponentGraveyard):
                    break
                index = random.randint(0, len(graveyard) + len(opponentGraveyard) - 1)
                if index <= len(graveyard) - 1:
                    cardData = graveyard[index]
                else:
                    index -= len(graveyard)
                    cardData = opponentGraveyard[index]

            copy = self.match.copyCard(cardData)
            targetUnit = Unit(copy)
            targetUnit.whiteFlag = self.whiteFlag
            targetUnit.setRow(row)
            targetIndex = len(row)
            row.insert(targetIndex, targetUnit)

            action = {}
            action['type'] = Action.MINION_FROM_GRAVEYEARD
            action['card'] = copy
            action['client'] = self.client
            action['initiatorIndex'] = targetIndex
            action['endAnimationFlag'] = True
            #Все поля заполнены правильно?????

            controller = Controller()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.addUnit(targetUnit)

            controller = Controller()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.unitPlaced (targetUnit)

            controller = CardController()
            controller.setWhiteFlag(self.whiteFlag)
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.new_unit()















    def beckCardToHand (self, targets, eptitude):

        if self.whiteFlag:
            hand = self.match.white_hand
            opponentHand = self.match.black_hand
            row = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
        else:
            hand = self.match.black_hand
            opponentHand = self.match.white_hand
            row = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow


        for target in targets:
            cardData = target.cardData

            if self.containsDynamicEptitudes (target):
                self.deactivateDynamic (target)

            selectAttachment = self.match.initAttachment (target, self.whiteFlag)
            selectIndex = self.match.initIndex (target, selectAttachment, self.whiteFlag)

            if target.whiteFlag == self.whiteFlag:
                hand.append(cardData)
                del row[selectIndex]
            else:
                opponentHand.append(cardData)
                del opponentRow[selectIndex]

            cardData['whiteFlag'] = target.whiteFlag

            action = {}
            action['targetIndex'] = selectIndex
            action['targetAttachment'] = selectAttachment
            action['type'] = Action.BACK_TOKEN_TO_HAND
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['card'] = self.match.copyCard(cardData)
            self.scenario.append (action)

            self.match.lastCardinHand = cardData
            self.match.configureLastCard (cardData)

            for unit in row:
                controller = Controller()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.newCard(unit)
                if cardData['whiteFlag'] == unit.whiteFlag:
                    controller.newPlayerCard(unit)
                else:
                    controller.newOpponentCard(unit)

            for unit in opponentRow:
                controller = Controller()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.newCard(unit)
                if cardData['whiteFlag'] == unit.whiteFlag:
                    controller.newPlayerCard(unit)
                else:
                    controller.newOpponentCard(unit)

            controller = CardController()
            controller.setWhiteFlag(self.whiteFlag)
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.new_card()


            if target.whiteFlag == self.whiteFlag:
                action = {}
                action['type'] = Action.GLOW_CARDS
                action['client'] = self.client
                action['endAnimationFlag'] = False
                self.scenario.append(action)

    def backSeveralTokensToHand (self, targets, eptitude):
        if len(targets):
            eptitude.activated = True
        else:
            return

        if self.whiteFlag:
            hand = self.match.white_hand
            opponentHand = self.match.black_hand
            row = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
        else:
            hand = self.match.black_hand
            opponentHand = self.match.white_hand
            row = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow

        associateBackCards = []
        associateBackCardsData = []
        opponentBackCards = []
        opponentBackCardsData = []
        destroyCards = []
        destroyCardsData = []

        for target in targets:

            card = self.match.getCardById(target.cardData['id'])
            cardData = self.match.getUnitCardData(card)
            cardData['whiteFlag'] = target.whiteFlag

            targetAttachment = self.match.initAttachment (target, self.whiteFlag)
            targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)

            if target.whiteFlag == self.whiteFlag:
                if eptitude.attachment == EptitudeAttachment.ASSOCIATE or eptitude.attachment == EptitudeAttachment.ALL:
                    handLength = len(hand)
                    if handLength < 10:
                        associateBackCards.append(target)
                        hand.append(cardData)

                        cardIndex = hand.index(cardData)
                        associateBackCardsData.append({'index':targetIndex, 'attachment':targetAttachment, 'card':cardData, 'cardIndex':cardIndex})
                    else:
                        destroyCards.append(target)
                        destroyCardsData.append({'index':targetIndex, 'attachment':targetAttachment, 'damage':target.getHealth()})
            else:
                if eptitude.attachment == EptitudeAttachment.OPPONENT or eptitude.attachment == EptitudeAttachment.ALL:
                    handLength = len(opponentHand)
                    if handLength < 10:
                        opponentBackCards.append(target)
                        opponentHand.append(cardData)

                        cardIndex = opponentHand.index(cardData)
                        opponentBackCardsData.append({'index':targetIndex, 'attachment':targetAttachment, 'card':cardData, 'cardIndex':cardIndex})
                    else:
                        destroyCards.append(target)
                        destroyCardsData.append({'index':targetIndex, 'attachment':targetAttachment, 'damage':target.getHealth()})




        action = {}
        action['type'] = Action.DAMAGE
        action['targets'] = destroyCardsData
        action['client'] = self.client
        self.scenario.append(action)

        action = {}
        action['type'] = Action.BACK_SEVERAL_TOKENS_TO_HAND
        action['associateTargets'] = associateBackCardsData
        action['opponentTargets'] = opponentBackCardsData
        action['deathTargets'] = destroyCardsData
        action['client'] = self.client
        self.scenario.append(action)




        for target in targets:
            try:
                targetIndex = row.index(target)
                del row[targetIndex]
            except:
                try:
                    targetIndex = opponentRow.index(target)
                    del opponentRow[targetIndex]
                except:
                    pass


        for target in associateBackCards:
            if self.containsDynamicEptitudes (target):
                self.deactivateDynamic (target)

        for target in opponentBackCards:
            if self.containsDynamicEptitudes (target):
                self.deactivateDynamic (target)


        # события вернувшихся юнитов
        for i in range(len(associateBackCards) + len(opponentBackCards)):
            for unit in row:
                controller = Controller()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.newCard(unit)
                if cardData['whiteFlag'] == unit.whiteFlag:
                    controller.newPlayerCard(unit)
                else:
                    controller.newOpponentCard(unit)

            for unit in opponentRow:
                controller = Controller()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.newCard(unit)
                if cardData['whiteFlag'] == unit.whiteFlag:
                    controller.newPlayerCard(unit)
                else:
                    controller.newOpponentCard(unit)

            controller = CardController()
            controller.setWhiteFlag(self.whiteFlag)
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.new_card()

        # события уничтоженных юнитов
        for targetUnit in destroyCards:
            controller = Controller()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.removeUnit(targetUnit)

            controller = CardController()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.unit_die(targetUnit.whiteFlag)

    def copyUnitCardsToHand (self, targets, eptitude):
        if len(targets):
            eptitude.activated = True
        else:
            return

        if self.whiteFlag:
            hand = self.match.white_hand
            opponentHand = self.match.black_hand
            row = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
        else:
            hand = self.match.black_hand
            opponentHand = self.match.white_hand
            row = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow

        associateBackCards = []
        associateBackCardsData = []
        opponentBackCards = []
        opponentBackCardsData = []

        for target in targets:

            card = self.match.getCardById(target.cardData['id'])
            cardData = self.match.getUnitCardData(card)
            cardData['whiteFlag'] = target.whiteFlag

            targetAttachment = self.match.initAttachment (target, self.whiteFlag)
            targetIndex = self.match.initIndex (target, targetAttachment, self.whiteFlag)

            if target.whiteFlag == self.whiteFlag:
                if eptitude.attachment == EptitudeAttachment.ASSOCIATE or eptitude.attachment == EptitudeAttachment.ALL:
                    handLength = len(hand)
                    if handLength < 10:
                        associateBackCards.append(target)
                        hand.append(cardData)

                        cardIndex = hand.index(cardData)
                        associateBackCardsData.append({'index':targetIndex, 'attachment':targetAttachment, 'card':cardData, 'cardIndex':cardIndex})

                if eptitude.attachment == EptitudeAttachment.OPPONENT or eptitude.attachment == EptitudeAttachment.ALL:
                    handLength = len(opponentHand)
                    if handLength < 10:
                        opponentBackCards.append(target)
                        opponentHand.append(cardData)

                        cardIndex = opponentHand.index(cardData)
                        opponentBackCardsData.append({'index':targetIndex, 'attachment':targetAttachment, 'card':cardData, 'cardIndex':cardIndex})

        action = {}
        action['type'] = Action.COPY_UNIT_CARDS_TO_HAND
        action['associateTargets'] = associateBackCardsData
        action['opponentTargets'] = opponentBackCardsData
        action['client'] = self.client
        self.scenario.append(action)


    def increase_a_h_depepend_on_tokens(self, targets, eptitude):
        power = eptitude.power
        for targetUnit in targets:
            if targetUnit.whiteFlag:
                row = self.match.whiteUnitRow
                opponentRow = self.match.blackUnitRow
            else:
                row = self.match.blackUnitRow
                opponentRow = self.match.whiteUnitRow


            if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
                total = power * len(row)
                if eptitude.attachInitiator == False:
                    total = total - 1 * power

            elif eptitude.attachment == EptitudeAttachment.OPPONENT:
                total = power * len(opponentRow)
            else:
                total = power * (len(row) + len(opponentRow))
                if eptitude.attachInitiator == False:
                    total = total - 1 * power


            targetUnit.setAttack(targetUnit.getAttack() + total)
            targetUnit.setHealth(targetUnit.getHealth() + total)
            targetUnit.setMaxHealth (targetUnit.getMaxHealth() + total)
            action = {}
            action['type'] = Action.INCREASE_ATTACK_AND_HEALTH
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action["power"] = total
            targetAttachment = self.match.initAttachment (targetUnit, self.whiteFlag)
            targetIndex = self.match.initIndex (targetUnit, targetAttachment, self.whiteFlag)
            action['targetIndex'] = targetIndex
            action['targetAttachment'] = targetAttachment
            self.scenario.append (action)

    def default_attack (self, targets, eptitude):
        for targetUnit in targets:
            targetUnit.setAttack (targetUnit.getDefaultAttack())
            attachment = self.match.initAttachment (targetUnit, self.whiteFlag)
            index = self.match.initIndex (targetUnit, attachment, self.whiteFlag)
            action = {}
            action['type'] = Action.INCREASE_ATTACK
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['attachment'] = attachment
            action['attack'] = targetUnit.getAttack()
            action['index'] = index
            self.scenario.append(action)

    def dumbness (self, targets, eptitude):
        if len(targets):
            eptitude.activated = True

        for targetUnit in targets:
            targetUnit.setAttack (targetUnit.getDefaultAttack())
            if targetUnit.getHealth() > targetUnit.defaultHealth:
                targetUnit.setHealth(targetUnit.defaultHealth)
            targetUnit.provocation = False
            if targetUnit.getAttack() > 0:
                targetUnit.canAttack = True
            else:
                targetUnit.canAttack = False
            if targetUnit.attackCount > 1:
                targetUnit.attackCount = 1
            targetUnit.jerk = False
            targetUnit.shield = False
            targetUnit.shadow = False
            targetUnit.doubleAttack = False
            targetUnit.freeze = False
            targetUnit.freezeIndex = 0
            targetUnit.dumbness = True
            targetUnit.spellUp = False
            targetUnit.spellInvisible = False

            controller = CardController()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.destroy_shield()
            controller.freeze()

            # деактивируем динамическую аттаку если есть таковая в способностях
            if self.containsDynamicEptitudes (targetUnit):
                self.deactivateDynamic (targetUnit)

            # убираем все способности
            targetUnit.eptitudes = []

            attachment = self.match.initAttachment (targetUnit, self.whiteFlag)
            index = self.match.initIndex (targetUnit, attachment, self.whiteFlag)
            action = {}
            action['type'] = Action.DUMBNESS
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['attachment'] = attachment
            action['attack'] = targetUnit.getAttack()
            action['health'] = targetUnit.getHealth()
            action['index'] = index
            action['attackCount'] = targetUnit.attackCount
            action['canAttack'] = targetUnit.canAttack
            self.scenario.append(action)

            if targetUnit.whiteFlag == self.whiteFlag and targetUnit.stepCount > 0 and targetUnit.canAttack:
                 action = {}
                 action['type'] = Action.ATTACK_AVAILABLE
                 action['client'] = self.client
                 action['endAnimationFlag'] = False
                 da_units = []
                 da_units.append (targetUnit.row.index(targetUnit))
                 action['unitList'] = da_units
                 self.scenario.append(action)

                 action = {}
                 action['type'] = Action.GLOW_UNITS
                 action['client'] = self.client
                 action['endAnimationFlag'] = False
                 self.scenario.append(action)



    def treatment (self, targets, eptitude):
        power = eptitude.power

        if eptitude.spellSensibility:
            if self.whiteFlag:
                spellMixin = self.match.whiteSpellMixin
            else:
                spellMixin = self.match.blackSpellMixin
            power += spellMixin


        logger.debug ('treatment power:%s, targets:%s' % (power, len(targets)))

        for targetUnit in targets:

            if targetUnit.getHealth() == targetUnit.maxHealth:
                pass
            else:
                targetUnit.treatment (power)

                targetAttachment = self.match.initAttachment (targetUnit, self.whiteFlag)
                targetIndex = self.match.initIndex (targetUnit, targetAttachment, self.whiteFlag)

                action = {}
                action['type'] = Action.TREATMENT
                action['client'] = self.client
                action['endAnimationFlag'] = False
                action['index'] = targetIndex
                action['attachment'] = targetAttachment
                action["health"] = targetUnit.getHealth()
                self.scenario.append(action)

                try:
                    self.match.whiteUnitRow.index(targetUnit)
                    playerRow = self.match.whiteUnitRow
                    opponentRow = self.match.blackUnitRow
                    playerHero = self.match.getWhiteHero()
                    opponentHero = self.match.getBlackHero()
                except:
                    playerRow = self.match.blackUnitRow
                    opponentRow = self.match.whiteUnitRow
                    playerHero = self.match.getBlackHero()
                    opponentHero = self.match.getWhiteHero()

                controller = Controller()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)

                if isinstance(targetUnit, HeroUnit):
                    if targetUnit == playerHero:
                        controller.treatHero(playerRow, True)
                        controller.treatHero(opponentRow, False)
                    else:
                        controller.treatHero(playerRow, False)
                        controller.treatHero(opponentRow, True)

                    controller.treatHeroes (playerRow, opponentRow)
                else:
                    controller.treatAssociate(playerRow)
                    controller.treatOpponent(opponentRow)
                    controller.treatAll(playerRow, opponentRow)

                if isinstance (targetUnit, Unit):
                    if targetUnit.getHealth() == targetUnit.getMaxHealth():
                         controller = Controller()
                         controller.setMatch(self.match)
                         controller.setScenario(self.scenario)
                         controller.setClient(self.client)
                         controller.setWhiteFlag(self.whiteFlag)
                         controller.fullHealthUnit(targetUnit)


    def treatHero (self, row, playerFlag):
         for item in row:
              self.unit = item
              self.eptitudes = item.eptitudes[:]
              if playerFlag:
                  self.activate (EptitudePeriod.ASSOCIATE_HERO_TREATED)
              else:
                  self.activate (EptitudePeriod.OPPONENT_HERO_TREATED)

    def treatHeroes (self, playerRow, opponentRow):
         for item in playerRow:
              self.unit = item
              self.eptitudes = item.eptitudes[:]
              self.activate (EptitudePeriod.ALL_HEROES_TREATED)

         for item in opponentRow:
              self.unit = item
              self.eptitudes = item.eptitudes[:]
              self.activate (EptitudePeriod.ALL_HEROES_TREATED)

    def treatAssociate (self, row):
         for item in row:
              self.unit = item
              self.eptitudes = item.eptitudes[:]
              self.activate (EptitudePeriod.ASSOCIATE_TREATED)

    def treatOpponent (self, row):
         for item in row:
              self.unit = item
              self.eptitudes = item.eptitudes[:]
              self.activate (EptitudePeriod.OPPONENT_TREATED)

    def treatAll (self, playerRow, opponentRow):
         for item in playerRow:
              self.unit = item
              self.eptitudes = item.eptitudes[:]
              self.activate (EptitudePeriod.ALL_TREATED)

         for item in opponentRow:
              self.unit = item
              self.eptitudes = item.eptitudes[:]
              self.activate (EptitudePeriod.ALL_TREATED)




    def kill(self, unit, targets, eptitude):
        if len(targets):
            eptitude.activated = True

        for targetUnit in targets:
            targetAttachment = self.match.initAttachment (targetUnit, self.whiteFlag)
            targetIndex = self.match.initIndex (targetUnit, targetAttachment, self.whiteFlag)

            if targetIndex >= 0:
                if isinstance (targetUnit, Unit):
                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.woundUnit(targetUnit)

                action = {}
                action['type'] = Action.DAMAGE
                action['client'] = self.client
                action['targets'] = [{'index':targetIndex, 'attachment':targetAttachment, 'damage':targetUnit.getHealth()}]
                self.scenario.append(action)

                self.match.buryMinion(targetUnit)

                self.match.deleteUnit (targetIndex, targetAttachment, self.whiteFlag)
                action = {}
                action['type'] = Action.TOKEN_DEATH
                action['client'] = self.client
                action['endAnimationFlag'] = True
                action['targetIndex'] = targetIndex
                action['targetAttachment'] = targetAttachment
                self.scenario.append(action)

                self.match.dieUnitsIndex += 1

                controller = Controller()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.removeUnit(targetUnit)

                controller = CardController()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.unit_die(targetUnit.whiteFlag)

            else:
                #logger.debug ('addAction::opponent_hero_death')
                action = {}
                action['type'] = Action.HERO_DEATH
                action['client'] = self.client
                action['endAnimationFlag'] = True
                action['targetAttachment'] = targetAttachment
                self.scenario.append(action)

            if self.whiteFlag:
                rowLength = len (self.match.whiteUnitRow)
            else:
                rowLength = len (self.match.blackUnitRow)

            action = {}
            action['type'] = Action.SET_ROW_LENGTH
            action['client'] = self.client
            action['length'] = rowLength
            self.scenario.append (action)

    def massive_kill (self, targets, eptitude):
        if len(targets):
            eptitude.activated = True
        else:
            return

        scenarioTargets = []

        # создаем объекты для их последующей ликвиданции и анимации урона
        for targetUnit in targets:
            targetAttachment = self.match.initAttachment (targetUnit, self.whiteFlag)
            targetIndex = self.match.initIndex (targetUnit, targetAttachment, self.whiteFlag)
            targetData = {}
            targetData['index'] = targetIndex
            targetData['attachment'] = targetAttachment
            targetData['damage'] = targetUnit.getHealth()
            scenarioTargets.append(targetData)

        action = {}
        action['type'] = Action.DAMAGE
        action['client'] = self.client
        action['targets'] = scenarioTargets
        self.scenario.append(action)

        # проганяем все цели по событиям урона
        for targetUnit in targets:
            if targetIndex >= 0:
                if isinstance (targetUnit, Unit):
                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.woundUnit(targetUnit)

        # уничтожаем все фишки на клиенте
        action = {}
        action['type'] = Action.MASSIVE_KILL
        action['client'] = self.client
        action['targets'] = scenarioTargets
        self.scenario.append(action)

        # уничтожаем все фишки на сервере и прогоняем их по событиям смерти
        for targetUnit in targets:
            if targetIndex >= 0:

                self.match.buryMinion(targetUnit)

                targetAttachment = self.match.initAttachment (targetUnit, self.whiteFlag)
                targetIndex = self.match.initIndex (targetUnit, targetAttachment, self.whiteFlag)
                self.match.deleteUnit (targetIndex, targetAttachment, self.whiteFlag)

                self.match.dieUnitsIndex += 1

                controller = Controller()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.removeUnit(targetUnit)

                controller = CardController()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.unit_die(targetUnit.whiteFlag)


    def passive_attack_series (self, unit, eptitude):
        count = eptitude.power

        heroDeath = False

        if eptitude.spellSensibility:
            if unit.whiteFlag:
                spellMixin = self.match.whiteSpellMixin
            else:
                spellMixin = self.match.blackSpellMixin
            count = spellMixin + count

        attackValue = 1
        for i in range(count):
            targetUnit = self.match.getLevelTargets(unit, eptitude, unit.whiteFlag)[0]
            self.match.lastAttacked = targetUnit
            targetHealthValue = targetUnit.getHealth()

            if targetUnit.shield and attackValue > 0:
                targetUnit.shield = False
                targetNewHealthValue = targetHealthValue
                action = {}
                action['type'] = Action.DESTROY_SHIELD
                action['client'] = self.client
                attachment = self.match.initAttachment (targetUnit, self.whiteFlag)
                index = self.match.initIndex (targetUnit, attachment, self.whiteFlag)
                action['index'] = index
                action['attachment'] = attachment
                action['endAnimationFlag'] = False
                shieldActionFlag = True
                shieldAction = action

                controller = CardController()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.destroy_shield()

            else:
                shieldActionFlag = False
                targetNewHealthValue = targetHealthValue - attackValue
                targetUnit.setHealth(targetNewHealthValue)

            initiatorAttachment = self.match.initAttachment (unit, self.whiteFlag)
            initiatorIndex = self.match.initIndex (unit, initiatorAttachment, self.whiteFlag)

            targetAttachment = self.match.initAttachment (targetUnit, self.whiteFlag)
            targetIndex = self.match.initIndex (targetUnit, targetAttachment, self.whiteFlag)

            if initiatorAttachment == -1 and initiatorIndex == -1:
                initiatorAttachment = targetAttachment
                initiatorIndex = targetIndex

            action = {}
            action['type'] = Action.PASSIVE_ATTACK
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['initiatorAttachment'] = initiatorAttachment
            action['initiatorIndex'] = initiatorIndex
            action['targetIndex'] = targetIndex
            action['targetAttachment'] = targetAttachment
            self.scenario.append(action)

            if not shieldActionFlag:
                action = {}
                action['type'] = Action.DAMAGE
                action['client'] = self.client
                action['targets'] = [{'index':targetIndex, 'attachment':targetAttachment, 'damage':attackValue}]
                self.scenario.append(action)

            action = {}
            action['type'] = Action.HEALTH_AFTER_PASSIVE_ATTACK
            action['client'] = self.client
            action['endAnimationFlag'] = False
            action['targetIndex'] = targetIndex
            action['targetAttachment'] = targetAttachment
            action["targetUnitHealth"] = targetUnit.getHealth()
            self.scenario.append(action)

            if shieldActionFlag:
                self.scenario.append (shieldAction)

            if targetNewHealthValue < targetHealthValue:
                if isinstance (targetUnit, Unit):
                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.woundUnit(targetUnit)

                if isinstance(targetUnit, HeroUnit):
                    controller = CardController()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.hero_wound(targetUnit.whiteFlag)


            if targetUnit.getHealth() <=0:
                if targetIndex >= 0:

                    self.match.buryMinion(targetUnit)

                    if targetUnit.hasSelfDieEptitude():
                             action = {}
                             action['type'] = Action.ACTIVATE_WIDGET
                             action['client'] = self.client
                             action['targetIndex'] = targetIndex
                             action['targetAttachment'] = targetAttachment
                             self.scenario.append(action)

                    self.match.deleteUnit (targetIndex, targetAttachment, self.whiteFlag)
                    action = {}
                    action['type'] = Action.TOKEN_DEATH
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    action['targetIndex'] = targetIndex
                    action['targetAttachment'] = targetAttachment
                    self.scenario.append(action)

                    self.match.dieUnitsIndex += 1

                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.removeUnit(targetUnit)

                    controller = CardController()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.unit_die(targetUnit.whiteFlag)

                else:
                    #logger.debug ('addAction::opponent_hero_death')
                    heroDeath = True

        if self.whiteFlag:
            rowLength = len (self.match.whiteUnitRow)
        else:
            rowLength = len (self.match.blackUnitRow)



        action = {}
        action['type'] = Action.SET_ROW_LENGTH
        action['client'] = self.client
        action['length'] = rowLength
        self.scenario.append (action)

        if heroDeath:
            self.match.endMatch(self.client, self.scenario, self.whiteFlag)



    def passive_attack (self, unit, targets, eptitude):
        if len(targets):
            eptitude.activated = True

        attackValue = eptitude.power

        heroDeath = False

        if eptitude.max_power:
            randomPower = random.randint(attackValue, eptitude.max_power)
            attackValue = randomPower

        if eptitude.spellSensibility:
            logger.debug('eptitude.spellSensibility')
            if unit.whiteFlag:
                spellMixin = self.match.whiteSpellMixin
            else:
                spellMixin = self.match.blackSpellMixin
            attackValue =  attackValue + spellMixin

        for targetUnit in targets:
            self.match.lastAttacked = targetUnit
            if isinstance(targetUnit, Unit):
                self.match.lastAttackedUnit = targetUnit
            targetHealthValue = targetUnit.getHealth()
            if targetUnit.shield and attackValue > 0:
                targetUnit.shield = False
                targetNewHealthValue = targetHealthValue
                action = {}
                action['type'] = Action.DESTROY_SHIELD
                action['client'] = self.client
                attachment = self.match.initAttachment (targetUnit, self.whiteFlag)
                index = self.match.initIndex (targetUnit, attachment, self.whiteFlag)
                action['index'] = index
                action['attachment'] = attachment
                action['endAnimationFlag'] = False
                shieldActionFlag = True
                shieldAction = action

                controller = CardController()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.destroy_shield()

            else:
                shieldActionFlag = False
                targetNewHealthValue = targetHealthValue - attackValue
                targetUnit.setHealth(targetNewHealthValue)

            initiatorAttachment = self.match.initAttachment (unit, self.whiteFlag)
            logger.debug ('initiatorAttachment: %s' % initiatorAttachment)
            initiatorIndex = self.match.initIndex (unit, initiatorAttachment, self.whiteFlag)
            logger.debug ('initiatorIndex: %s' % initiatorIndex)

            targetAttachment = self.match.initAttachment (targetUnit, self.whiteFlag)
            logger.debug ('targetAttachment: %s' % targetAttachment)
            targetIndex = self.match.initIndex (targetUnit, targetAttachment, self.whiteFlag)
            logger.debug ('targetIndex: %s' % targetIndex)

            if initiatorAttachment == -1 and initiatorIndex == -1:
                initiatorAttachment = targetAttachment
                initiatorIndex = targetIndex

            action = {}
            action['type'] = Action.PASSIVE_ATTACK
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['initiatorAttachment'] = initiatorAttachment
            action['initiatorIndex'] = initiatorIndex
            action['targetIndex'] = targetIndex
            action['targetAttachment'] = targetAttachment
            self.scenario.append(action)

            if not shieldActionFlag:
                action = {}
                action['type'] = Action.DAMAGE
                action['client'] = self.client
                action['targets'] = [{'index':targetIndex, 'attachment':targetAttachment, 'damage':attackValue}]
                self.scenario.append(action)


            action = {}
            action['type'] = Action.HEALTH_AFTER_PASSIVE_ATTACK
            action['client'] = self.client
            action['endAnimationFlag'] = False
            action['targetIndex'] = targetIndex
            action['targetAttachment'] = targetAttachment
            action["targetUnitHealth"] = targetUnit.getHealth()
            self.scenario.append(action)

            if shieldActionFlag:
                self.scenario.append (shieldAction)

            if targetNewHealthValue < targetHealthValue:
                if isinstance (targetUnit, Unit):
                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.woundUnit(targetUnit)

                if isinstance(targetUnit, HeroUnit):
                    controller = CardController()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.hero_wound(targetUnit.whiteFlag)


            if targetUnit.getHealth() <=0:
                if targetIndex >= 0:

                    self.match.buryMinion(targetUnit)

                    if targetUnit.hasSelfDieEptitude():
                             action = {}
                             action['type'] = Action.ACTIVATE_WIDGET
                             action['client'] = self.client
                             action['targetIndex'] = targetIndex
                             action['targetAttachment'] = targetAttachment
                             self.scenario.append(action)

                    self.match.deleteUnit (targetIndex, targetAttachment, self.whiteFlag)
                    action = {}
                    action['type'] = Action.TOKEN_DEATH
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    action['targetIndex'] = targetIndex
                    action['targetAttachment'] = targetAttachment
                    self.scenario.append(action)

                    self.match.dieUnitsIndex += 1

                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.removeUnit(targetUnit)

                    controller = CardController()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.unit_die(targetUnit.whiteFlag)

                else:
                    #logger.debug ('addAction::opponent_hero_death')
                   heroDeath = True

        if self.whiteFlag:
            rowLength = len (self.match.whiteUnitRow)
        else:
            rowLength = len (self.match.blackUnitRow)

        action = {}
        action['type'] = Action.SET_ROW_LENGTH
        action['client'] = self.client
        action['length'] = rowLength
        self.scenario.append (action)

        if heroDeath:
            self.match.endMatch(self.client, self.scenario, self.whiteFlag)

    def getNotSameRandow (self, unit, eptitude, targets):
         levelTargets = self.match.getLevelTargets(unit, eptitude, unit.whiteFlag)
         target = levelTargets[0]
         targetFlag = False
         try:
             index = targets.index(target)
             targetFlag = True
         except:
             pass

         if targetFlag:
             return  self.getNotSameRandow(unit, eptitude, targets)
         else:
             return target


    def passive_attack_for_several_targets (self, unit, eptitude):
        logger.debug ('passive_attack_for_several_targets')
        targets = []
        targetsIndexes = []
        for i in range (eptitude.count):
            target = self.getNotSameRandow(unit, eptitude, targets)
            targets.append(target)
            targetData = {}
            attachment = self.match.initAttachment (target, self.whiteFlag)
            targetData['attachment'] = attachment
            targetData['index'] = self.match.initIndex (target, attachment, self.whiteFlag)
            targetsIndexes.append (targetData)


        initiatorAttachment = self.match.initAttachment (unit, self.whiteFlag)
        initiatorIndex = self.match.initIndex (unit, initiatorAttachment, self.whiteFlag)

        logger.debug ('targetIndexes.length:%s' % len(targetsIndexes))

        action = {}
        action['type'] = Action.PASSIVE_ATTACK_FOR_SEVERAL_TARGETS
        action['client'] = self.client
        action['endAnimationFlag'] = True
        action['initiatorAttachment'] = initiatorAttachment
        action['initiatorIndex'] = initiatorIndex
        action['targets'] = targetsIndexes
        self.scenario.append(action)

        attackValue = eptitude.power

        if eptitude.spellSensibility:
            logger.debug('eptitude.spellSensibility')
            if unit.whiteFlag:
                spellMixin = self.match.whiteSpellMixin
            else:
                spellMixin = self.match.blackSpellMixin
            attackValue =  attackValue + spellMixin

        for targetUnit in targets:
            targetHealthValue = targetUnit.getHealth()
            if targetUnit.shield and attackValue > 0:
                targetUnit.shield = False
                targetNewHealthValue = targetHealthValue

                action = {}
                action['type'] = Action.DESTROY_SHIELD
                action['client'] = self.client
                attachment = self.match.initAttachment (targetUnit, self.whiteFlag)
                index = self.match.initIndex (targetUnit, attachment, self.whiteFlag)
                action['index'] = index
                action['attachment'] = attachment
                action['endAnimationFlag'] = False
                shieldActionFlag = True
                shieldAction = action

                controller = CardController()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.destroy_shield()

            else:

                shieldActionFlag = False
                targetNewHealthValue = targetHealthValue - attackValue
                targetUnit.setHealth(targetNewHealthValue)

            targetAttachment = self.match.initAttachment (targetUnit, self.whiteFlag)
            targetIndex = self.match.initIndex (targetUnit, targetAttachment, self.whiteFlag)

            if not shieldActionFlag:
                action = {}
                action['type'] = Action.DAMAGE
                action['client'] = self.client
                action['targets'] = [{'index':targetIndex, 'attachment':targetAttachment, 'damage':attackValue}]
                self.scenario.append(action)

            action = {}
            action['type'] = Action.HEALTH_AFTER_PASSIVE_ATTACK
            action['client'] = self.client
            action['endAnimationFlag'] = False
            action['targetIndex'] = targetIndex
            action['targetAttachment'] = targetAttachment
            action["targetUnitHealth"] = targetUnit.getHealth()
            self.scenario.append(action)

            if shieldActionFlag:
                self.scenario.append (shieldAction)

            if targetNewHealthValue < targetHealthValue:
                if isinstance (targetUnit, Unit):
                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.woundUnit(targetUnit)

                if isinstance(targetUnit, HeroUnit):
                    controller = CardController()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.hero_wound(targetUnit.whiteFlag)

            if targetUnit.getHealth() <=0:
                if targetIndex >= 0:

                    self.match.buryMinion(targetUnit)

                    if targetUnit.hasSelfDieEptitude():
                         action = {}
                         action['type'] = Action.ACTIVATE_WIDGET
                         action['client'] = self.client
                         action['targetIndex'] = targetIndex
                         action['targetAttachment'] = targetAttachment
                         self.scenario.append(action)

                    self.match.deleteUnit (targetIndex, targetAttachment, self.whiteFlag)
                    action = {}
                    action['type'] = Action.TOKEN_DEATH
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    action['targetIndex'] = targetIndex
                    action['targetAttachment'] = targetAttachment
                    self.scenario.append(action)

                    self.match.dieUnitsIndex += 1

                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.removeUnit(targetUnit)

                    controller = CardController()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.unit_die(targetUnit.whiteFlag)

                else:
                    action = {}
                    action['type'] = Action.HERO_DEATH
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    action['targetAttachment'] = targetAttachment
                    self.scenario.append(action)








    def freeze_attack (self, unit, targets, eptitude):
        if len(targets):
            eptitude.activated = True

        attackValue = eptitude.power

        heroDeath = False

        if eptitude.max_power:
            randomPower = random.randint(attackValue, eptitude.max_power)
            attackValue = randomPower

        for targetUnit in targets:

            if eptitude.spellSensibility:
                if unit.whiteFlag:
                    spellMixin = self.match.whiteSpellMixin
                else:
                    spellMixin = self.match.blackSpellMixin
                attackValue += spellMixin

            targetHealthValue = targetUnit.getHealth()
            if targetUnit.shield and attackValue > 0:
                targetUnit.shield = False
                targetNewHealthValue = targetHealthValue
                action = {}
                action['type'] = Action.DESTROY_SHIELD
                action['client'] = self.client
                attachment = self.match.initAttachment (targetUnit, self.whiteFlag)
                index = self.match.initIndex (targetUnit, attachment, self.whiteFlag)
                action['index'] = index
                action['attachment'] = attachment
                action['endAnimationFlag'] = False
                shieldActionFlag = True
                shieldAction = action

                controller = CardController()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.destroy_shield()

            else:
                shieldActionFlag = False
                targetNewHealthValue = targetHealthValue - attackValue
                targetUnit.setHealth(targetNewHealthValue)

            targetUnit.freeze = True
            targetUnit.freezeIndex = 2

            controller = CardController()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.freeze()

            initiatorAttachment = self.match.initAttachment (unit, self.whiteFlag)
            logger.debug ('initiatorAttachment: %s' % initiatorAttachment)
            initiatorIndex = self.match.initIndex (unit, initiatorAttachment, self.whiteFlag)
            logger.debug ('initiatorIndex: %s' % initiatorIndex)

            targetAttachment = self.match.initAttachment (targetUnit, self.whiteFlag)
            logger.debug ('targetAttachment: %s' % targetAttachment)
            targetIndex = self.match.initIndex (targetUnit, targetAttachment, self.whiteFlag)
            logger.debug ('targetIndex: %s' % targetIndex)

            if initiatorAttachment == -1 and initiatorIndex == -1:
                initiatorAttachment = targetAttachment
                initiatorIndex = targetIndex

            action = {}
            action['type'] = Action.FREEZE_ATTACK
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['initiatorAttachment'] = initiatorAttachment
            action['initiatorIndex'] = initiatorIndex
            action['targetIndex'] = targetIndex
            action['targetAttachment'] = targetAttachment
            action['animation'] = eptitude.animation
            logger.debug ('animation: %s' % (action['animation']))

            self.scenario.append(action)

            if not shieldActionFlag:
                action = {}
                action['type'] = Action.DAMAGE
                action['client'] = self.client
                action['targets'] = [{'index':targetIndex, 'attachment':targetAttachment, 'damage':attackValue}]
                self.scenario.append(action)

            action = {}
            action['type'] = Action.HEALTH_AFTER_PASSIVE_ATTACK
            action['client'] = self.client
            action['endAnimationFlag'] = False
            action['targetIndex'] = targetIndex
            action['targetAttachment'] = targetAttachment
            action["targetUnitHealth"] = targetUnit.getHealth()
            self.scenario.append(action)

            if shieldActionFlag:
                self.scenario.append (shieldAction)

            if targetNewHealthValue < targetHealthValue:
                if isinstance (targetUnit, Unit):
                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.woundUnit(targetUnit)

                if isinstance(targetUnit, HeroUnit):
                    controller = CardController()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.hero_wound(targetUnit.whiteFlag)

            if targetUnit.getHealth() <=0:
                if targetIndex >= 0:

                    self.match.buryMinion(targetUnit)

                    if targetUnit.hasSelfDieEptitude():
                         action = {}
                         action['type'] = Action.ACTIVATE_WIDGET
                         action['client'] = self.client
                         action['targetIndex'] = targetIndex
                         action['targetAttachment'] = targetAttachment
                         self.scenario.append(action)

                    self.match.deleteUnit (targetIndex, targetAttachment, self.whiteFlag)
                    action = {}
                    action['type'] = Action.TOKEN_DEATH
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    action['targetIndex'] = targetIndex
                    action['targetAttachment'] = targetAttachment
                    self.scenario.append(action)

                    self.match.dieUnitsIndex += 1

                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.removeUnit(targetUnit)

                    controller = CardController()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.unit_die(targetUnit.whiteFlag)

                else:
                    #logger.debug ('addAction::opponent_hero_death')
                   heroDeath = True

        if self.whiteFlag:
            rowLength = len (self.match.whiteUnitRow)
        else:
            rowLength = len (self.match.blackUnitRow)

        action = {}
        action['type'] = Action.SET_ROW_LENGTH
        action['client'] = self.client
        action['length'] = rowLength
        self.scenario.append (action)

        if heroDeath:
            self.match.endMatch(self.client, self.scenario, self.whiteFlag)

    def freeze (self, targets, eptitude):

        if len(targets):
            eptitude.activated = True


        for targetUnit in targets:

            targetUnit.freeze = True
            targetUnit.freezeIndex = 2

            controller = CardController()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.freeze()

            targetAttachment = self.match.initAttachment (targetUnit, self.whiteFlag)
            logger.debug ('targetAttachment: %s' % targetAttachment)
            targetIndex = self.match.initIndex (targetUnit, targetAttachment, self.whiteFlag)
            logger.debug ('targetIndex: %s' % targetIndex)

            action = {}
            action['type'] = Action.FREEZE
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['index'] = targetIndex
            action['attachment'] = targetAttachment
            self.scenario.append(action)



    def massive_attack (self, unit, targets, eptitude):
        if len(targets):
            eptitude.activated = True
        else:
            return

        attackValue = eptitude.power
        heroDeath = False

        if eptitude.max_power:
            randomPower = random.randint(attackValue, eptitude.max_power)
            attackValue = randomPower

        if eptitude.spellSensibility:
                if unit.whiteFlag:
                    spellMixin = self.match.whiteSpellMixin
                else:
                    spellMixin = self.match.blackSpellMixin
                attackValue += spellMixin

        if attackValue <= 0:
            return

        scenarioTargets = []
        shieldTargets = []
        woundTargets = []

        for targetUnit in targets:
            attachment = self.match.initAttachment (targetUnit, self.whiteFlag)
            index = self.match.initIndex (targetUnit, attachment, self.whiteFlag)
            if targetUnit.shield:
                shieldTargets.append(targetUnit)
                scenarioTargets.append({'index':index,'attachment':attachment,'damage':0, 'health':targetUnit.getHealth()})
            else:
                targetHealthValue = targetUnit.getHealth()
                targetNewHealthValue = targetHealthValue - attackValue
                targetUnit.setHealth(targetNewHealthValue)
                scenarioTargets.append({'index':index,'attachment':attachment,'damage':attackValue, 'health':targetUnit.getHealth()})
                woundTargets.append(targetUnit)

        action = {}
        action['type'] = Action.DAMAGE
        action['client'] = self.client
        action['targets'] = scenarioTargets
        action['endAnimationFlag'] = True
        self.scenario.append(action)

        action = {}
        action['type'] = Action.MASSIVE_ATTACK
        action['targets'] = scenarioTargets
        action['client'] = self.client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

        for targetUnit in shieldTargets:
            targetUnit.shield = False
            action = {}
            action['type'] = Action.DESTROY_SHIELD
            action['client'] = self.client
            attachment = self.match.initAttachment (targetUnit, self.whiteFlag)
            index = self.match.initIndex (targetUnit, attachment, self.whiteFlag)
            action['index'] = index
            action['attachment'] = attachment
            action['endAnimationFlag'] = False
            self.scenario.append(action)

            controller = CardController()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.destroy_shield()

        scenarioTargets = []
        deathUnits = []

        logger.debug('woundTargets.length:%s' % len(woundTargets))

        for targetUnit in woundTargets:
            if isinstance (targetUnit, Unit):
                controller = Controller()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.woundUnit(targetUnit)

            if isinstance(targetUnit, HeroUnit):
                controller = CardController()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.hero_wound(targetUnit.whiteFlag)

            if targetUnit.getHealth() <=0:
                attachment = self.match.initAttachment (targetUnit, self.whiteFlag)
                index = self.match.initIndex (targetUnit, attachment, self.whiteFlag)

                if index >= 0:
                    scenarioTargets.append({'index':index, 'attachment':attachment})
                    deathUnits.append(targetUnit)
                else:
                    heroDeath = True

        action = {}
        action['type'] = Action.MASSIVE_KILL
        action['client'] = self.client
        action['targets'] = scenarioTargets
        self.scenario.append(action)

        logger.debug('Action.MASSIVE_KILL')
        logger.debug(scenarioTargets)

        for targetUnit in deathUnits:
            self.match.buryMinion(targetUnit)
            attachment = self.match.initAttachment (targetUnit, self.whiteFlag)
            index = self.match.initIndex (targetUnit, attachment, self.whiteFlag)
            self.match.deleteUnit (index, attachment, self.whiteFlag)
            self.match.dieUnitsIndex += 1

        for targetUnit in deathUnits:
            controller = Controller()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.removeUnit(targetUnit)

            controller = CardController()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.unit_die(targetUnit.whiteFlag)

        if self.whiteFlag:
            rowLength = len (self.match.whiteUnitRow)
        else:
            rowLength = len (self.match.blackUnitRow)

        action = {}
        action['type'] = Action.SET_ROW_LENGTH
        action['client'] = self.client
        action['length'] = rowLength
        self.scenario.append (action)

        if heroDeath:
            self.match.endMatch(self.client, self.scenario, self.whiteFlag)

    def massive_attack_depends_on_target_attack_value(self, targets, eptitude):
        if len(targets):
            eptitude.activated = True
        else:
            return

        scenarioTargets = []
        shieldTargets = []
        woundTargets = []

        attackValue = 0

        for targetUnit in targets:
            attachment = self.match.initAttachment (targetUnit, self.whiteFlag)
            index = self.match.initIndex (targetUnit, attachment, self.whiteFlag)
            if targetUnit.shield:
                shieldTargets.append(targetUnit)
                scenarioTargets.append({'index':index,'attachment':attachment,'damage':0, 'health':targetUnit.getHealth()})
            else:
                targetHealthValue = targetUnit.getHealth()
                attackValue = targetUnit.getAttack()
                targetNewHealthValue = targetHealthValue - attackValue
                targetUnit.setHealth(targetNewHealthValue)
                scenarioTargets.append({'index':index,'attachment':attachment,'damage':attackValue, 'health':targetUnit.getHealth()})
                woundTargets.append(targetUnit)

        action = {}
        action['type'] = Action.DAMAGE
        action['client'] = self.client
        action['targets'] = scenarioTargets
        action['endAnimationFlag'] = True
        self.scenario.append(action)

        action = {}
        action['type'] = Action.MASSIVE_ATTACK
        action['targets'] = scenarioTargets
        action['client'] = self.client
        action['endAnimationFlag'] = False
        self.scenario.append(action)

        for targetUnit in shieldTargets:
            targetUnit.shield = False
            action = {}
            action['type'] = Action.DESTROY_SHIELD
            action['client'] = self.client
            attachment = self.match.initAttachment (targetUnit, self.whiteFlag)
            index = self.match.initIndex (targetUnit, attachment, self.whiteFlag)
            action['index'] = index
            action['attachment'] = attachment
            action['endAnimationFlag'] = False
            self.scenario.append(action)

            controller = CardController()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.destroy_shield()

        scenarioTargets = []
        deathUnits = []

        for targetUnit in woundTargets:
            if isinstance (targetUnit, Unit):
                controller = Controller()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.woundUnit(targetUnit)

            if isinstance(targetUnit, HeroUnit):
                controller = CardController()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.hero_wound(targetUnit.whiteFlag)

            if targetUnit.getHealth() <=0:
                attachment = self.match.initAttachment (targetUnit, self.whiteFlag)
                index = self.match.initIndex (targetUnit, attachment, self.whiteFlag)

                if index >= 0:
                    scenarioTargets.append({'index':index, 'attachment':attachment})
                    deathUnits.append(targetUnit)
                else:
                    action = {}
                    action['type'] = Action.HERO_DEATH
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    action['targetAttachment'] = attachment
                    self.scenario.append(action)

        action = {}
        action['type'] = Action.MASSIVE_KILL
        action['client'] = self.client
        action['targets'] = scenarioTargets
        self.scenario.append(action)

        logger.debug('Action.MASSIVE_KILL')
        logger.debug(scenarioTargets)

        for targetUnit in deathUnits:
            attachment = self.match.initAttachment (targetUnit, self.whiteFlag)
            index = self.match.initIndex (targetUnit, attachment, self.whiteFlag)
            self.match.deleteUnit (index, attachment, self.whiteFlag)
            self.match.dieUnitsIndex += 1

        for targetUnit in deathUnits:
            self.match.buryMinion(targetUnit)
            controller = Controller()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.removeUnit(targetUnit)

            controller = CardController()
            controller.setMatch(self.match)
            controller.setScenario(self.scenario)
            controller.setClient(self.client)
            controller.setWhiteFlag(self.whiteFlag)
            controller.unit_die(targetUnit.whiteFlag)

        if self.whiteFlag:
            rowLength = len (self.match.whiteUnitRow)
        else:
            rowLength = len (self.match.blackUnitRow)

        action = {}
        action['type'] = Action.SET_ROW_LENGTH
        action['client'] = self.client
        action['length'] = rowLength
        self.scenario.append (action)

    def pick_card (self, targets, eptitude, count):

        if not len(targets):
            return

        unitFlag = self.unit.getWhiteFlag()
        unit = self.unit
        if self.whiteFlag:
            row = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
        else:
            row = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow


        if unit.whiteFlag:
            hand = self.match.white_hand
            opponentHand = self.match.black_hand
        else:
            hand = self.match.black_hand
            opponentHand = self.match.white_hand

        for i in range(count):
            attachment = eptitude.attachment
            pickFlag = False
            if attachment == EptitudeAttachment.ASSOCIATE:
                if self.match.deckLength(unitFlag):
                        if len(hand) < 10:
                            card = self.match.getCard(unitFlag, True)
                            cardCopy = self.match.copyCard(card)
                            action = {}
                            action['type'] = Action.PICK_CARD
                            action['client'] = self.client
                            if self.whiteFlag == unitFlag:
                                action['attachment'] = EptitudeAttachment.ASSOCIATE
                            else:
                                action['attachment'] = EptitudeAttachment.OPPONENT
                            action['card'] = cardCopy
                            action['endAnimationFlag'] = True
                            self.scenario.append(action)
                            pickFlag = True
                            if self.match.getMode() == 2:
                                action = {}
                                action['type'] = Action.SHIFT_DECK_SLOT
                                action['client'] = self.client
                                if self.whiteFlag == unitFlag:
                                    action['attachment'] = EptitudeAttachment.ASSOCIATE
                                else:
                                    action['attachment'] = EptitudeAttachment.OPPONENT
                                self.scenario.append(action)
                        else:
                            if self.match.burnExtraCardsFlag:
                                card = self.match.getCard(unitFlag, False)
                                cardCopy = self.match.copyCard(card)
                                action = {}
                                action['type'] = Action.BURN_CARD
                                if self.whiteFlag == unitFlag:
                                    action['attachment'] = EptitudeAttachment.ASSOCIATE
                                else:
                                    action['attachment'] = EptitudeAttachment.OPPONENT
                                action['client'] = self.client
                                action['card'] = cardCopy
                                action['endAnimationFlag'] = True
                                self.scenario.append(action)
                                pickFlag = False

                else:
                    if self.match.attritionFlag:
                         self.match.attrition(self.client, unitFlag, False)

                if pickFlag:

                    self.match.calculateCards(self.client, self.scenario, self.whiteFlag)

                    action = {}
                    action['type'] = Action.GLOW_CARDS
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    self.scenario.append(action)

                    self.match.lastCardinHand = card
                    self.match.configureLastCard (card)

                    for unit in row:
                        controller = Controller()
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.newCard(unit)
                        if card['whiteFlag'] == unit.whiteFlag:
                            controller.newPlayerCard(unit)
                        else:
                            controller.newOpponentCard(unit)

                    for unit in opponentRow:
                        controller = Controller()
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.newCard(unit)
                        if card['whiteFlag'] == unit.whiteFlag:
                            controller.newPlayerCard(unit)
                        else:
                            controller.newOpponentCard(unit)

                    controller = CardController()
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.new_card()


            elif attachment == EptitudeAttachment.OPPONENT:
                if self.match.deckLength(not unitFlag):
                        if len(opponentHand) < 10:
                            card = self.match.getCard(not unitFlag, True)
                            cardCopy = self.match.copyCard(card)
                            action = {}
                            action['type'] = Action.PICK_CARD
                            action['client'] = self.client
                            if self.whiteFlag == unitFlag:
                                action['attachment'] = EptitudeAttachment.OPPONENT
                            else:
                                action['attachment'] = EptitudeAttachment.ASSOCIATE
                            action['card'] = cardCopy
                            action['endAnimationFlag'] = True
                            self.scenario.append(action)
                            pickFlag = True
                            if self.match.getMode() == 2:
                                action = {}
                                action['type'] = Action.SHIFT_DECK_SLOT
                                action['client'] = self.client
                                if self.whiteFlag == unitFlag:
                                    action['attachment'] = EptitudeAttachment.OPPONENT
                                else:
                                    action['attachment'] = EptitudeAttachment.ASSOCIATE
                                self.scenario.append(action)
                        else:
                            if self.match.burnExtraCardsFlag:
                                card = self.match.getCard(not unitFlag, False)
                                cardCopy = self.match.copyCard(card)
                                action = {}
                                action['type'] = Action.BURN_CARD
                                if self.whiteFlag == unitFlag:
                                    action['attachment'] = EptitudeAttachment.OPPONENT
                                else:
                                    action['attachment'] = EptitudeAttachment.ASSOCIATE
                                action['client'] = self.client
                                action['card'] = cardCopy
                                action['endAnimationFlag'] = True
                                self.scenario.append(action)
                                pickFlag = False

                else:
                    if self.match.attritionFlag:
                         self.match.attrition(self.client,not unitFlag, True)

                if pickFlag:
                    self.match.lastCardinHand = card
                    self.match.configureLastCard (card)

                    self.match.calculateCards(self.client, self.scenario, self.whiteFlag)

                    for unit in row:
                        controller = Controller()
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.newCard(unit)
                        if card['whiteFlag'] == unit.whiteFlag:
                            controller.newPlayerCard(unit)
                        else:
                            controller.newOpponentCard(unit)

                    for unit in opponentRow:
                        controller = Controller()
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.newCard(unit)
                        if card['whiteFlag'] == unit.whiteFlag:
                            controller.newPlayerCard(unit)
                        else:
                            controller.newOpponentCard(unit)

                    controller = CardController()
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.new_card()

            elif attachment == EptitudeAttachment.ALL:

                pickFlag = False
                if self.match.deckLength(unitFlag):
                        if len(hand) < 10:
                            card = self.match.getCard(unitFlag, True)
                            cardCopy = self.match.copyCard(card)
                            action = {}
                            action['type'] = Action.PICK_CARD
                            action['client'] = self.client
                            if self.whiteFlag == unitFlag:
                                action['attachment'] = EptitudeAttachment.ASSOCIATE
                            else:
                                action['attachment'] = EptitudeAttachment.OPPONENT
                            action['card'] = cardCopy
                            action['endAnimationFlag'] = True
                            self.scenario.append(action)
                            pickFlag = True
                            if self.match.getMode() == 2:
                                action = {}
                                action['type'] = Action.SHIFT_DECK_SLOT
                                action['client'] = self.client
                                if self.whiteFlag == unitFlag:
                                    action['attachment'] = EptitudeAttachment.ASSOCIATE
                                else:
                                    action['attachment'] = EptitudeAttachment.OPPONENT
                                self.scenario.append(action)
                        else:
                            if self.match.burnExtraCardsFlag:
                                card = self.match.getCard(unitFlag, False)
                                cardCopy = self.match.copyCard(card)
                                action = {}
                                action['type'] = Action.BURN_CARD
                                if self.whiteFlag == unitFlag:
                                    action['attachment'] = EptitudeAttachment.ASSOCIATE
                                else:
                                    action['attachment'] = EptitudeAttachment.OPPONENT
                                action['client'] = self.client
                                action['card'] = cardCopy
                                action['endAnimationFlag'] = True
                                self.scenario.append(action)
                                pickFlag = False

                else:
                    if self.match.attritionFlag:
                         self.match.attrition(self.client, unitFlag, False)

                if pickFlag:

                    action = {}
                    action['type'] = Action.GLOW_CARDS
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    self.scenario.append(action)

                    self.match.calculateCards(self.client, self.scenario, self.whiteFlag)

                    self.match.lastCardinHand = card
                    self.match.configureLastCard (card)

                    for unit in row:
                        controller = Controller()
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.newCard(unit)
                        if card['whiteFlag'] == unit.whiteFlag:
                            controller.newPlayerCard(unit)
                        else:
                            controller.newOpponentCard(unit)

                    for unit in opponentRow:
                        controller = Controller()
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.newCard(unit)
                        if card['whiteFlag'] == unit.whiteFlag:
                            controller.newPlayerCard(unit)
                        else:
                            controller.newOpponentCard(unit)

                    controller = CardController()
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.new_card()


                pickFlag = False
                if self.match.deckLength(not unitFlag):
                        if len(opponentHand) < 10:
                            card2 = self.match.getCard(not unitFlag, True)
                            card2Copy = self.match.copyCard(card2)
                            action = {}
                            action['type'] = Action.PICK_CARD
                            action['client'] = self.client
                            if self.whiteFlag == unitFlag:
                                action['attachment'] = EptitudeAttachment.OPPONENT
                            else:
                                action['attachment'] = EptitudeAttachment.ASSOCIATE
                            action['card'] = card2Copy
                            action['endAnimationFlag'] = True
                            self.scenario.append(action)
                            pickFlag = True
                            if self.match.getMode() == 2:
                                action = {}
                                action['type'] = Action.SHIFT_DECK_SLOT
                                action['client'] = self.client
                                if self.whiteFlag == unitFlag:
                                    action['attachment'] = EptitudeAttachment.OPPONENT
                                else:
                                    action['attachment'] = EptitudeAttachment.ASSOCIATE
                                self.scenario.append(action)
                        else:
                            if self.match.burnExtraCardsFlag:
                                card = self.match.getCard(not unitFlag, False)
                                cardCopy = self.match.copyCard(card)
                                action = {}
                                action['type'] = Action.BURN_CARD
                                if self.whiteFlag == unitFlag:
                                    action['attachment'] = EptitudeAttachment.OPPONENT
                                else:
                                    action['attachment'] = EptitudeAttachment.ASSOCIATE
                                action['client'] = self.client
                                action['card'] = cardCopy
                                action['endAnimationFlag'] = True
                                self.scenario.append(action)
                                pickFlag = False

                else:
                    if self.match.attritionFlag:
                         self.match.attrition(self.client,not unitFlag, True)

                if pickFlag:
                    self.match.lastCardinHand = card2
                    self.match.configureLastCard (card2)

                    self.match.calculateCards(self.client, self.scenario, self.whiteFlag)

                    for unit in row:
                        controller = Controller()
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.newCard(unit)
                        if card2['whiteFlag'] == unit.whiteFlag:
                            controller.newPlayerCard(unit)
                        else:
                            controller.newOpponentCard(unit)

                    for unit in opponentRow:
                        controller = Controller()
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.newCard(unit)
                        if card2['whiteFlag'] == unit.whiteFlag:
                            controller.newPlayerCard(unit)
                        else:
                            controller.newOpponentCard(unit)

                    controller = CardController()
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.new_card()





    def pick_card_till(self, targets, eptitude):
        for target in targets:
            if target == self.match.whiteHeroUnit:
                hand = self.match.white_hand
                row = self.match.whiteUnitRow
                opponentRow = self.match.blackUnitRow
            else:
                hand = self.match.black_hand
                row = self.match.blackUnitRow
                opponentRow = self.match.whiteUnitRow

            if len(hand) < eptitude.power:
                count = eptitude.power - len(hand)

                for i in range(count):
                    pickFlag = False
                    if self.match.deckLength(target.whiteFlag):
                        if len(hand) < 10:
                            card = self.match.getCard(target.whiteFlag, True)
                            cardCopy = self.match.copyCard(card)
                            action = {}
                            action['type'] = Action.PICK_CARD
                            action['client'] = self.client
                            if self.whiteFlag == target.whiteFlag:
                                action['attachment'] = EptitudeAttachment.ASSOCIATE
                            else:
                                action['attachment'] = EptitudeAttachment.OPPONENT
                            action['card'] = cardCopy
                            action['endAnimationFlag'] = True
                            self.scenario.append(action)
                            pickFlag = True
                            if self.match.getMode() == 2:
                                action = {}
                                action['type'] = Action.SHIFT_DECK_SLOT
                                action['client'] = self.client
                                if self.whiteFlag == target.whiteFlag:
                                    action['attachment'] = EptitudeAttachment.ASSOCIATE
                                else:
                                    action['attachment'] = EptitudeAttachment.OPPONENT
                                self.scenario.append(action)
                        else:
                            if self.match.burnExtraCardsFlag:
                                card = self.match.getCard(target.whiteFlag, False)
                                cardCopy = self.match.copyCard(card)
                                action = {}
                                action['type'] = Action.BURN_CARD
                                if self.whiteFlag == target.whiteFlag:
                                    action['attachment'] = EptitudeAttachment.ASSOCIATE
                                else:
                                    action['attachment'] = EptitudeAttachment.OPPONENT
                                action['client'] = self.client
                                action['card'] = cardCopy
                                action['endAnimationFlag'] = True
                                self.scenario.append(action)
                                pickFlag = False

                    else:
                        if self.match.attritionFlag:
                             self.match.attrition(self.client, target.whiteFlag, False)


                    if pickFlag:
                        self.match.lastCardinHand = card
                        self.match.configureLastCard (card)

                        self.match.calculateCards(self.client, self.scenario, self.whiteFlag)

                        for unit in row:
                            controller = Controller()
                            controller.setMatch(self.match)
                            controller.setScenario(self.scenario)
                            controller.setClient(self.client)
                            controller.setWhiteFlag(self.whiteFlag)
                            controller.newCard(unit)
                            if card['whiteFlag'] == unit.whiteFlag:
                                controller.newPlayerCard(unit)
                            else:
                                controller.newOpponentCard(unit)

                        for unit in opponentRow:
                            controller = Controller()
                            controller.setMatch(self.match)
                            controller.setScenario(self.scenario)
                            controller.setClient(self.client)
                            controller.setWhiteFlag(self.whiteFlag)
                            controller.newCard(unit)
                            if card['whiteFlag'] == unit.whiteFlag:
                                controller.newPlayerCard(unit)
                            else:
                                controller.newOpponentCard(unit)

                        controller = CardController()
                        controller.setWhiteFlag(self.whiteFlag)
                        controller.setMatch(self.match)
                        controller.setScenario(self.scenario)
                        controller.setClient(self.client)
                        controller.new_card()

    def pick_card_depends_on_wound_units(self, targets, eptitude):
        if len(targets):
           eptitude.activated = True
        else:
           return

        if self.whiteFlag:
            hero = self.match.whiteHeroUnit
            row = self.match.whiteUnitRow
            opponentHero = self.match.blackHeroUnit
            opponentRow = self.match.blackUnitRow
        else:
            opponentHero = self.match.whiteHeroUnit
            hero = self.match.blackHeroUnit
            row = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow

        count = 0

        if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
            for unit in row:
                if unit.getHealth() < unit.getMaxHealth():
                    count += 1
            if eptitude.attachHero and hero.getHealth() < hero.getMaxHealth():
                    count += 1

        if eptitude.attachment == EptitudeAttachment.OPPONENT:
            for unit in opponentRow:
                if unit.getHealth() < unit.getMaxHealth():
                    count += 1
            if eptitude.attachHero and opponentHero.getHealth() < opponentHero.getMaxHealth():
                    count += 1

        target = targets[0]
        if target.whiteFlag:
             hand = self.match.white_hand
        else:
             hand = self.match.black_hand

        for i in range(count):
            pickFlag = False
            if self.match.deckLength(target.whiteFlag):
                if len(hand) < 10:
                    card = self.match.getCard(target.whiteFlag, True)
                    cardCopy = self.match.copyCard(card)
                    action = {}
                    action['type'] = Action.PICK_CARD
                    action['client'] = self.client
                    if self.whiteFlag == target.whiteFlag:
                        action['attachment'] = EptitudeAttachment.ASSOCIATE
                    else:
                        action['attachment'] = EptitudeAttachment.OPPONENT
                    action['card'] = cardCopy
                    action['endAnimationFlag'] = True
                    self.scenario.append(action)
                    pickFlag = True
                    if self.match.getMode() == 2:
                        action = {}
                        action['type'] = Action.SHIFT_DECK_SLOT
                        action['client'] = self.client
                        if self.whiteFlag == target.whiteFlag:
                            action['attachment'] = EptitudeAttachment.ASSOCIATE
                        else:
                            action['attachment'] = EptitudeAttachment.OPPONENT
                        self.scenario.append(action)
                else:
                    if self.match.burnExtraCardsFlag:
                        card = self.match.getCard(target.whiteFlag, False)
                        cardCopy = self.match.copyCard(card)
                        action = {}
                        action['type'] = Action.BURN_CARD
                        if self.whiteFlag == target.whiteFlag:
                            action['attachment'] = EptitudeAttachment.ASSOCIATE
                        else:
                            action['attachment'] = EptitudeAttachment.OPPONENT
                        action['client'] = self.client
                        action['card'] = cardCopy
                        action['endAnimationFlag'] = True
                        self.scenario.append(action)
                        pickFlag = False

            else:
                if self.match.attritionFlag:
                     self.match.attrition(self.client, target.whiteFlag, False)

            if pickFlag:

                self.match.lastCardinHand = card
                self.match.configureLastCard (card)

                self.match.calculateCards(self.client, self.scenario, self.whiteFlag)

                for unit in row:
                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.newCard(unit)
                    if card['whiteFlag'] == unit.whiteFlag:
                        controller.newPlayerCard(unit)
                    else:
                        controller.newOpponentCard(unit)

                for unit in opponentRow:
                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.newCard(unit)
                    if card['whiteFlag'] == unit.whiteFlag:
                        controller.newPlayerCard(unit)
                    else:
                        controller.newOpponentCard(unit)

                controller = CardController()
                controller.setWhiteFlag(self.whiteFlag)
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.new_card()

    def pick_card_depends_on_opponent_cards_count (self, targets, eptitude):
        if len(targets):
           eptitude.activated = True
        else:
           return

        if self.whiteFlag:
            hand = self.match.white_hand
            opponentHand = self.match.black_hand
            row = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
        else:
            hand = self.match.black_hand
            opponentHand = self.match.white_hand
            row = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow

        count = len(opponentHand)
        count = count - len(hand)

        target = targets[0]

        for i in range(count):
            if len(hand) >= len(opponentHand):
                return

            pickFlag = False
            if self.match.deckLength(target.whiteFlag):
                if len(hand) < 10:
                        card = self.match.getCard(target.whiteFlag, True)
                        cardCopy = self.match.copyCard(card)
                        action = {}
                        action['type'] = Action.PICK_CARD
                        action['client'] = self.client
                        if self.whiteFlag == target.whiteFlag:
                            action['attachment'] = EptitudeAttachment.ASSOCIATE
                        else:
                            action['attachment'] = EptitudeAttachment.OPPONENT
                        action['card'] = cardCopy
                        action['endAnimationFlag'] = True
                        self.scenario.append(action)
                        pickFlag = True
                        if self.match.getMode() == 2:
                            action = {}
                            action['type'] = Action.SHIFT_DECK_SLOT
                            action['client'] = self.client
                            if self.whiteFlag == target.whiteFlag:
                                action['attachment'] = EptitudeAttachment.ASSOCIATE
                            else:
                                action['attachment'] = EptitudeAttachment.OPPONENT
                            self.scenario.append(action)
                else:
                        if self.match.burnExtraCardsFlag:
                            card = self.match.getCard(target.whiteFlag, False)
                            cardCopy = self.match.copyCard(card)
                            action = {}
                            action['type'] = Action.BURN_CARD
                            if self.whiteFlag == target.whiteFlag:
                                action['attachment'] = EptitudeAttachment.ASSOCIATE
                            else:
                                action['attachment'] = EptitudeAttachment.OPPONENT
                            action['client'] = self.client
                            action['card'] = cardCopy
                            action['endAnimationFlag'] = True
                            self.scenario.append(action)
                            pickFlag = False

            else:
                 if self.match.attritionFlag:
                     self.match.attrition(self.client, target.whiteFlag, False)


            if pickFlag:
                self.match.lastCardinHand = card
                self.match.configureLastCard (card)

                self.match.calculateCards(self.client, self.scenario, self.whiteFlag)

                for unit in row:
                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.newCard(unit)
                    if card['whiteFlag'] == unit.whiteFlag:
                        controller.newPlayerCard(unit)
                    else:
                        controller.newOpponentCard(unit)

                for unit in opponentRow:
                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.newCard(unit)
                    if card['whiteFlag'] == unit.whiteFlag:
                        controller.newPlayerCard(unit)
                    else:
                        controller.newOpponentCard(unit)

                controller = CardController()
                controller.setWhiteFlag(self.whiteFlag)
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.new_card()


    def rebirth (self, targets, eptitude):
        if len(targets):
           eptitude.activated = True
        else:
           return

        count = eptitude.power

        for target in targets:
            cardData = self.match.copyCard(self.unit.cardData)
            if target.whiteFlag:
                targetRow = self.match.whiteUnitRow
                opponentRow = self.match.blackUnitRow
            else:
                targetRow = self.match.blackUnitRow
                opponentRow = self.match.whiteUnitRow

            for i in range(count):
                if eptitude.attachment == EptitudeAttachment.ASSOCIATE and len(targetRow) < 7:
                    targetUnit = Unit(cardData)
                    targetUnit.setRow(targetRow)
                    targetUnit.setWhiteFlag(target.whiteFlag)
                    try:
                        targetIndex = targetRow.index(target) + 1
                    except:
                        if isinstance (self.unit, HeroUnit):
                            targetIndex = len(targetRow)
                        else:
                            targetIndex = target.index
                    targetRow.insert (targetIndex, targetUnit)
                    attachment = self.match.initAttachment (targetUnit, self.whiteFlag)
                    action = {}
                    action['type'] = Action.NEW_UNIT
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    action['attachment'] = attachment
                    action['index'] = targetIndex
                    action['cardData'] = cardData
                    self.scenario.append(action)

                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.addUnit(targetUnit)

                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.unitPlaced (targetUnit)

                    controller = CardController()
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.new_unit()

                if eptitude.attachment == EptitudeAttachment.OPPONENT and len(opponentRow) < 7:

                    targetUnit = Unit(cardData)
                    targetUnit.setRow(opponentRow)
                    targetUnit.setWhiteFlag(not target.whiteFlag)
                    targetIndex = len(opponentRow)
                    opponentRowRow.insert (targetIndex, targetUnit)
                    attachment = self.match.initAttachment (targetUnit, self.whiteFlag)

                    action = {}
                    action['type'] = Action.NEW_UNIT
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    action['attachment'] = attachment
                    action['index'] = targetIndex
                    action['cardData'] = cardData
                    self.scenario.append(action)

                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.addUnit(targetUnit)

                    controller = Controller()
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.unitPlaced (targetUnit)

                    controller = CardController()
                    controller.setWhiteFlag(self.whiteFlag)
                    controller.setMatch(self.match)
                    controller.setScenario(self.scenario)
                    controller.setClient(self.client)
                    controller.new_unit()

    def new_unit (self, unit, targets, eptitude):

        logger.debug ('new_unit targets.len:%s' % len(targets))

        if len(targets):
           eptitude.activated = True
        else:
           return

        count = eptitude.power

        if self.whiteFlag:
            playerRow = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
        else:
            playerRow = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow

        unitFlag = self.unit.getWhiteFlag()

        if self.whiteFlag == unitFlag:
            inverseFlag = False
        else:
            inverseFlag = True

        logger.debug ('inverseFlag:%s' % inverseFlag)

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
                groupId = eptitude.group
                group = Group.objects.get(id=groupId)
                index = random.randint(0, len(group.cards) - 1)
                unitCard = group.cards[index]
            except:
                pass
            try:
                cardId = eptitude.unit
                unitCard = Card.objects.get(id=cardId)
            except: pass

            if eptitude.price > - 1:
                try:
                    unitCard = random.choice(Card.objects.filter(price=eptitude.price, type=CardType.UNIT))
                    logger.debug(unitCard)
                except: pass

            targetRows = []
            # определяемся с рядом
            if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
                # уточняем общее количество в ряду
                if inverseFlag:
                    if len(opponentRow) < 7:
                        targetRows.append (opponentRow)
                else:
                    if len(playerRow) < 7:
                        targetRows.append (playerRow)


            elif eptitude.attachment == EptitudeAttachment.OPPONENT:
                if inverseFlag:
                    if len(playerRow) < 7:
                        targetRows.append (playerRow)
                else:
                    if len(opponentRow) < 7:
                        targetRows.append (opponentRow)

            else:
                if len(playerRow) < 7:
                    targetRows.append (playerRow)
                if len(opponentRow) < 7:
                    targetRows.append (opponentRow)


            # уточняем индексы
            try:
                playerIndex = playerRow.index(unit) + 1
            except:
                if isinstance (unit, HeroUnit):
                    playerIndex = len(playerRow)
                else:
                    playerIndex = unit.index

            if inverseFlag:
                try:
                    opponentIndex = opponentRow.index(unit) + 1
                except:
                    if isinstance (unit, HeroUnit):
                        opponentIndex = len(opponentRow)
                    else:
                        opponentIndex = unit.index
            else:
                opponentIndex = len(opponentRow)

            # добавляем в ряд
            cardData = self.match.getUnitCardData(unitCard)
            for row in targetRows:
                targetUnit = Unit(cardData)
                targetUnit.setRow(row)
                targetUnit.destroyBattlecryEptitudes()
                if row == playerRow:
                    row.insert (playerIndex, targetUnit)
                    if row == self.match.whiteUnitRow:
                        targetUnit.setWhiteFlag(True)
                    else:
                        targetUnit.setWhiteFlag(False)

                    attachment = self.match.initAttachment (targetUnit, self.whiteFlag)

                    # записываем в сценарий
                    action = {}
                    action['type'] = Action.NEW_UNIT
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    action['attachment'] = attachment
                    action['index'] = playerIndex
                    action['cardData'] = cardData
                    self.scenario.append(action)

                else:
                    row.insert (opponentIndex, targetUnit)
                    if row == self.match.whiteUnitRow:
                        targetUnit.setWhiteFlag(True)
                    else:
                        targetUnit.setWhiteFlag(False)

                    attachment = self.match.initAttachment (targetUnit, self.whiteFlag)
                    # записываем в сценарий
                    action = {}
                    action['type'] = Action.NEW_UNIT
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    action['attachment'] = attachment
                    action['index'] = opponentIndex
                    action['cardData'] = cardData
                    self.scenario.append(action)

                controller = Controller()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.addUnit(targetUnit)

                controller = Controller()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.unitPlaced (targetUnit)

                controller = CardController()
                controller.setWhiteFlag(self.whiteFlag)
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.new_unit()

        if self.whiteFlag:
            rowLength = len (self.match.whiteUnitRow)
        else:
            rowLength = len (self.match.blackUnitRow)

        action = {}
        action['type'] = Action.SET_ROW_LENGTH
        action['client'] = self.client
        action['length'] = rowLength
        self.scenario.append (action)

    def increase_attack (self, targets, eptitude):
        power = eptitude.power
        for target in targets:
            attachment = self.match.initAttachment (target, self.whiteFlag)
            index = self.match.initIndex (target, attachment, self.whiteFlag)

            noAttackFlag = False
            if target.getAttack() == 0 and target.stepCount > 0 and self.whiteFlag == target.whiteFlag:
                noAttackFlag = True

            target.setAttack (target.getAttack() + power)
            action = {}
            action['type'] = Action.INCREASE_ATTACK
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['attachment'] = attachment
            action['attack'] = target.getAttack()
            action['index'] = index
            self.scenario.append(action)

            if noAttackFlag:
                 action = {}
                 action['type'] = Action.ATTACK_AVAILABLE
                 action['client'] = self.client
                 action['endAnimationFlag'] = False
                 da_units = []
                 da_units.append (target.row.index(target))
                 action['unitList'] = da_units
                 self.scenario.append(action)

                 action = {}
                 action['type'] = Action.GLOW_UNITS
                 action['client'] = self.client
                 action['endAnimationFlag'] = False
                 self.scenario.append(action)

    def decrease_attack (self, targets, eptitude):
        power = eptitude.power
        for target in targets:
            attachment = self.match.initAttachment (target, self.whiteFlag)
            index = self.match.initIndex (target, attachment, self.whiteFlag)

            target.setAttack (target.getAttack() - power)
            action = {}
            action['type'] = Action.INCREASE_ATTACK
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['attachment'] = attachment
            action['attack'] = target.getAttack()
            action['index'] = index
            self.scenario.append(action)


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

    def increase_health_mixin (self, targets, eptitude):
        power = eptitude.power
        for target in targets:
            attachment = self.match.initAttachment (target, self.whiteFlag)
            index = self.match.initIndex (target, attachment, self.whiteFlag)

            newHealth = target.getHealth()
            newHealth += power
            target.setHealth (newHealth)
            target.setMaxHealth (target.getMaxHealth() + power)
            action = {}
            action['type'] = Action.INCREASE_HEALTH
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['attachment'] = attachment
            action['value'] = newHealth
            action['index'] = index
            self.scenario.append(action)



    def increase_health_depends_on_associate_cards (self, targets, eptitude):
         for target in targets:
            if target.whiteFlag:
                hand = self.match.white_hand
            else:
                hand = self.match.black_hand

            power = len(hand)

            attachment = self.match.initAttachment (target, self.whiteFlag)
            index = self.match.initIndex (target, attachment, self.whiteFlag)

            newHealth = target.getHealth()
            newHealth += power
            target.setHealth (newHealth)
            target.setMaxHealth (target.getMaxHealth() + power)
            action = {}
            action['type'] = Action.CHANGE_HEALTH
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['attachment'] = attachment
            action['value'] = newHealth
            action['index'] = index
            self.scenario.append(action)

    def increase_health_depends_on_opponent_cards (self, targets, eptitude):
         for target in targets:
            if target.whiteFlag:
                hand = self.match.black_hand
            else:
                hand = self.match.white_hand

            power = len(hand)

            attachment = self.match.initAttachment (target, self.whiteFlag)
            index = self.match.initIndex (target, attachment, self.whiteFlag)

            newHealth = target.getHealth()
            newHealth += power
            target.setHealth (newHealth)
            target.setMaxHealth (target.getMaxHealth() + power)
            action = {}
            action['type'] = Action.CHANGE_HEALTH
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['attachment'] = attachment
            action['value'] = newHealth
            action['index'] = index
            self.scenario.append(action)


    def decrease_attack_mixin (self, targets, eptitude):
        power = eptitude.power * -1
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

    def decrease_health_mixin (self, targets, eptitude):
        power = eptitude.power
        for target in targets:
            attachment = self.match.initAttachment (target, self.whiteFlag)
            index = self.match.initIndex (target, attachment, self.whiteFlag)

            newHealth = target.getHealth()
            newHealth -= power
            if newHealth < 1:
                newHealth = 1
            target.setHealth (newHealth)
            target.setMaxHealth (target.getMaxHealth() - power)
            action = {}
            action['type'] = Action.INCREASE_HEALTH
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['attachment'] = attachment
            action['value'] = newHealth
            action['maxHealth'] = target.getMaxHealth()
            action['index'] = index
            self.scenario.append(action)

    def unit_from_deck (self, eptitude):
        count = eptitude.power

        unitFlag = self.unit.getWhiteFlag()

        if self.whiteFlag:
            playerRow = self.match.whiteUnitRow
            opponentRow = self.match.blackUnitRow
        else:
            playerRow = self.match.blackUnitRow
            opponentRow = self.match.whiteUnitRow

        if self.whiteFlag == unitFlag:
            inverseFlag = False
        else:
            inverseFlag = True

        for i in range(count):

            targetRows = []

            # определяем список всех невытянутых существ
            unitCards = self.match.getUnitCardsList(unitFlag)

            # определяем случайное существо
            cardsCount = len(unitCards)
            index = random.randint (0, cardsCount - 1)

            # вытягиваем его из колоды
            cardData = self.match.getCardByIndex (index, unitFlag)

            # добавляем на поле
            if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
                # уточняем общее количество в ряду
                if inverseFlag:
                    if len(opponentRow) < 7:
                        targetRows.append (opponentRow)
                else:
                    if len(playerRow) < 7:
                        targetRows.append (playerRow)


            elif eptitude.attachment == EptitudeAttachment.OPPONENT:
                if inverseFlag:
                    if len(playerRow) < 7:
                        targetRows.append (playerRow)
                else:
                    if len(opponentRow) < 7:
                        targetRows.append (opponentRow)

            else:
                if len(playerRow) < 7:
                    targetRows.append (playerRow)
                if len(opponentRow) < 7:
                    targetRows.append (opponentRow)

            playerIndex = len(playerRow)
            opponentIndex = len(opponentRow)

            for row in targetRows:
                targetUnit = Unit(cardData)
                targetUnit.destroyBattlecryEptitudes()

                if row == playerRow:
                    row.insert (playerIndex, targetUnit)
                    if row == self.match.whiteUnitRow:
                        targetUnit.setWhiteFlag(True)
                    else:
                        targetUnit.setWhiteFlag(False)
                    # записываем в сценарий
                    action = {}
                    action['type'] = Action.NEW_UNIT
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    action['attachment'] = 1
                    action['index'] = playerIndex
                    action['cardData'] = cardData
                    self.scenario.append(action)

                else:
                    row.insert (opponentIndex, targetUnit)
                    if row == self.match.whiteUnitRow:
                        targetUnit.setWhiteFlag(True)
                    else:
                        targetUnit.setWhiteFlag(False)
                    # записываем в сценарий
                    action = {}
                    action['type'] = Action.NEW_UNIT
                    action['client'] = self.client
                    action['endAnimationFlag'] = True
                    action['attachment'] = 0
                    action['index'] = opponentIndex
                    action['cardData'] = cardData
                    self.scenario.append(action)

                self.addUnit(targetUnit)
                self.unitPlaced (targetUnit)

        if self.whiteFlag:
            rowLength = len (self.match.whiteUnitRow)
        else:
            rowLength = len (self.match.blackUnitRow)

        action = {}
        action['type'] = Action.SET_ROW_LENGTH
        action['client'] = self.client
        action['length'] = rowLength
        self.scenario.append (action)

    def unit_copy_from_deck(self, targets, eptitude):
        if len(targets):
           eptitude.activated = True
        else:
            return

        if self.unit.whiteFlag:
            targetRow = self.match.whiteUnitRow
        else:
            targetRow = self.match.blackUnitRow

        if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
            unitFlag = self.unit.whiteFlag
        elif eptitude.attachment == EptitudeAttachment.OPPONENT:
            unitFlag = not self.unit.whiteFlag

        # определяем список всех невытянутых существ
        unitCards = self.match.getUnitCardsList(unitFlag)

        count = eptitude.power
        for i in range(count):

            if len(targetRow) < 7:
                # определяем случайное существо
                cardsCount = len(unitCards)
                index = random.randint (0, cardsCount - 1)
                cardData = unitCards[index]
                copy = self.match.copyCard(cardData)
                targetUnit = Unit(copy)
                targetIndex = len(targetRow)

                targetRow.insert (targetIndex, targetUnit)
                targetUnit.setWhiteFlag(self.unit.whiteFlag)
                # записываем в сценарий
                action = {}
                action['type'] = Action.NEW_UNIT
                action['client'] = self.client
                action['endAnimationFlag'] = True
                action['attachment'] = 1
                action['index'] = targetIndex
                action['cardData'] = copy
                self.scenario.append(action)

                controller = Controller()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.addUnit(targetUnit)

                controller = Controller()
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.setWhiteFlag(self.whiteFlag)
                controller.unitPlaced (targetUnit)

                controller = CardController()
                controller.setWhiteFlag(self.whiteFlag)
                controller.setMatch(self.match)
                controller.setScenario(self.scenario)
                controller.setClient(self.client)
                controller.new_unit()











    def increase_card_price(self, unit, targets, eptitude):
        value = eptitude.power
        logger.debug ('controller.increase_card_price for cards %s' % len(targets))

        for card in targets:
            attachment, index = self.match.initCardAttachment(card, self.whiteFlag)

            if index > - 1:
                # меняем цену в самой карте
                logger.debug('card.attachment :%s, card.index:%s' % (attachment, index))
                card['price'] += value

                # оповещаем клиент
                action = {}
                action['type'] = Action.CHANGE_CARD_PRICE
                action['client'] = self.client
                action['endAnimationFlag'] = True
                action['attachment'] = attachment
                action['index'] = index
                action['price'] = card['price']
                self.scenario.append(action)

    def decrease_card_price(self, unit, targets, eptitude):
        value = eptitude.power
        logger.debug ('controller.decrease_card_price for cards %s' % len(targets))
        logger.debug(self.match.lastCardinHand)

        for card in targets:
            attachment, index = self.match.initCardAttachment(card, self.whiteFlag)

            if index > - 1:

                # меняем цену в самой карте
                logger.debug('card.attachment :%s, card.index:%s' % (attachment, index))
                card['price'] -= value

                if card['price'] < 0:
                    card['price'] = 0


                # оповещаем клиент
                action = {}
                action['type'] = Action.CHANGE_CARD_PRICE
                action['client'] = self.client
                action['endAnimationFlag'] = True
                action['attachment'] = attachment
                action['index'] = index
                action['price'] = card['price']
                self.scenario.append(action)

                if self.whiteFlag:
                    row = self.match.whiteUnitRow
                else:
                    row = self.match.blackUnitRow

                if len(row) < 7:
                    action = {}
                    action['type'] = Action.GLOW_CARDS
                    action['client'] = self.client
                    action['endAnimationFlag'] = False
                    self.scenario.append(action)

    def increase_card_price_mixin(self, unit, targets, eptitude):
        value = eptitude.power
        logger.debug ('controller.increase_card_price for cards %s' % len(targets))

        for card in targets:
            attachment, index = self.match.initCardAttachment(card, self.whiteFlag)

            # меняем цену в самой карте
            logger.debug('card.attachment :%s, card.index:%s' % (attachment, index))
            card['priceMixin'] += value

            # оповещаем клиент
            action = {}
            action['type'] = Action.CHANGE_CARD_PRICE
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['attachment'] = attachment
            action['index'] = index
            action['price'] = card['price'] + card['priceMixin']
            self.scenario.append(action)

    def decrease_card_price_mixin(self, unit, targets, eptitude):
        value = eptitude.power
        logger.debug ('controller.decrease_card_price for cards %s' % len(targets))

        for card in targets:
            attachment, index = self.match.initCardAttachment(card, self.whiteFlag)

            # меняем цену в самой карте
            logger.debug('card.attachment :%s, card.index:%s' % (attachment, index))
            card['priceMixin'] -= value
            if card['price'] + card['priceMixin'] < 0:
                card['priceMixin'] = card['price'] * -1

            # оповещаем клиент
            action = {}
            action['type'] = Action.CHANGE_CARD_PRICE
            action['client'] = self.client
            action['endAnimationFlag'] = True
            action['attachment'] = attachment
            action['index'] = index
            action['price'] = card['price'] + card['priceMixin']
            self.scenario.append(action)

            if self.whiteFlag:
                row = self.match.whiteUnitRow
            else:
                row = self.match.blackUnitRow

            if len(row) < 7:
                action = {}
                action['type'] = Action.GLOW_CARDS
                action['client'] = self.client
                action['endAnimationFlag'] = False
                self.scenario.append(action)

    def increaseMana (self, targets, eptitude):
        if len(targets):
           eptitude.activated = True
        else:
            return

        value = eptitude.power

        if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
            if self.whiteFlag:
                self.match.white_step_price += value
                self.match.white_price += value
                if self.match.white_price > 10:
                    self.match.white_price = 10
                price = self.match.white_step_price

            else:
                self.match.black_step_price += value
                self.match.black_price += value
                if self.match.black_price > 10:
                    self.match.black_price = 10
                price = self.match.black_step_price


            action = {}
            action['type'] = Action.CHANGE_MANA
            action['client'] = self.client
            action['price'] = price
            action['overload'] = self.match.stepOverload
            action['attachment'] = EptitudeAttachment.ASSOCIATE
            action['endAnimationFlag'] = False
            self.scenario.append (action)

        if eptitude.attachment == EptitudeAttachment.OPPONENT:
            if self.whiteFlag:
                self.match.black_step_price += value
                price = self.match.black_step_price
                self.match.black_price += value
                if self.match.black_price > 10:
                    self.match.black_price = 10

            else:
                self.match.white_step_price += value
                self.match.white_price += value
                if self.match.white_price > 10:
                    self.match.white_price = 10
                price = self.match.white_step_price

            action = {}
            action['type'] = Action.CHANGE_MANA
            action['client'] = self.client
            action['price'] = price
            action['overload'] = self.match.stepOverload
            action['attachment'] = EptitudeAttachment.OPPONENT
            action['endAnimationFlag'] = False
            self.scenario.append (action)

        if eptitude.attachment == EptitudeAttachment.ALL:

            self.match.white_step_price += value
            self.match.black_step_price += value
            self.match.white_price += value
            if self.match.white_price > 10:
                self.match.white_price = 10
            self.match.black_price += value
            if self.match.black_price > 10:
                self.match.black_price = 10

            if self.whiteFlag:
                playerPrice = self.match.white_step_price
                opponentPrice = self.match.black_step_price
            else:
                opponentPrice = self.match.white_step_price
                playerPrice = self.match.black_step_price

            action = {}
            action['type'] = Action.CHANGE_MANA
            action['client'] = self.client
            action['playerPrice'] = playerPrice
            action['opponentPrice'] = opponentPrice
            action['overload'] = self.match.stepOverload
            action['attachment'] = EptitudeAttachment.ALL
            action['endAnimationFlag'] = False
            self.scenario.append (action)

        action = {}
        action['type'] = Action.GLOW_CARDS
        action['client'] = self.client
        action['endAnimationFlag'] = False
        self.scenario.append(action)


    def decreaseMana (self, targets, eptitude):
        if len(targets):
           eptitude.activated = True
        else:
            return

        value = eptitude.power

        whiteHeroFlag = False
        blackHeroFlag = False

        if eptitude.attachment == EptitudeAttachment.ASSOCIATE:
            if self.whiteFlag:
                self.match.white_step_price -= value
                if self.match.white_step_price < 0:
                    self.match.white_step_price = 0
                price = self.match.white_step_price
                self.match.white_price -= value
                if self.match.white_price < 0:
                    self.match.white_price = 0
                whiteHeroFlag = True

            else:
                self.match.black_step_price -= value
                if self.match.black_step_price < 0:
                    self.match.black_step_price = 0
                price = self.match.black_step_price
                self.match.black_price -= value
                if self.match.black_price < 0:
                    self.match.black_price = 0
                blackHeroFlag = True

            action = {}
            action['type'] = Action.CHANGE_MANA
            action['client'] = self.client
            action['price'] = price
            action['attachment'] = EptitudeAttachment.ASSOCIATE
            action['endAnimationFlag'] = False
            self.scenario.append (action)

        if eptitude.attachment == EptitudeAttachment.OPPONENT:
            if self.whiteFlag:
                self.match.black_step_price -= value
                if self.match.black_step_price < 0:
                    self.match.black_step_price = 0
                price = self.match.black_step_price
                self.match.black_price -= value
                if self.match.black_price < 0:
                    self.match.black_price = 0
                blackHeroFlag = True

            else:
                self.match.white_step_price -= value
                if self.match.white_step_price < 0:
                    self.match.white_step_price = 0
                price = self.match.white_step_price
                self.match.white_price -= value
                if self.match.white_price < 0:
                    self.match.white_price = 0
                whiteHeroFlag = True

            action = {}
            action['type'] = Action.CHANGE_MANA
            action['client'] = self.client
            action['price'] = price
            action['attachment'] = EptitudeAttachment.OPPONENT
            action['endAnimationFlag'] = False
            self.scenario.append (action)

        if eptitude.attachment == EptitudeAttachment.ALL:

            whiteHeroFlag = True
            blackHeroFlag = True

            self.match.white_step_price -= value
            self.match.black_step_price -= value

            if self.match.white_step_price < 0:
                    self.match.white_step_price = 0
            if self.match.black_step_price < 0:
                    self.match.black_step_price = 0

            if self.match.black_price < 0:
                    self.match.black_price = 0
            if self.match.white_price < 0:
                    self.match.white_price = 0

            if self.whiteFlag:
                playerPrice = self.match.white_step_price
                opponentPrice = self.match.black_step_price
            else:
                opponentPrice = self.match.white_step_price
                playerPrice = self.match.black_step_price

            action = {}
            action['type'] = Action.CHANGE_MANA
            action['client'] = self.client
            action['playerPrice'] = playerPrice
            action['opponentPrice'] = opponentPrice
            action['attachment'] = EptitudeAttachment.ALL
            action['endAnimationFlag'] = False
            self.scenario.append (action)

            '''
            if eptitude.lifecycle > 0:
                if whiteHeroFlag:
                    self.match.whiteHeroUnit.appendTempEptitude (eptitude)

                if blackHeroFlag:
                    self.match.blackHeroUnit.appendTempEptitude (eptitude)
            '''

        action = {}
        action['type'] = Action.GLOW_CARDS
        action['client'] = self.client
        action['endAnimationFlag'] = False
        self.scenario.append(action)























