__author__ = 'RIK'
import logging
logger =  logging.getLogger('game_handler')

from card.models import Race, SubRace
from game.logic.constants import EptitudePeriod

class Weapon ():
      def __init__(self):
          self.power = 0
          self.strength = 0
          self.id = 0

class HeroUnit ():

     def __init__(self, health):
        self.health = health
        self.defaultHealth = health
        self.maxHealth = self.health
        self.defaultAttack = 0
        self.extraAttack = 0
        self.shield = False
        self.shadow = False
        self.doubleAttack = False
        self.freeze = False
        self.freezeIndex = 0
        self.whiteFlag = True
        self.tempEptitudes = []
        self.eptitudes = []
        self.spellInvisible = False
        self.spellUp = False
        self.stepAttackCount = 0
        self.fly = False
        self.rightHand = None
        self.leftHand = None


     def takeUpWeapon(self, weaponData):
        weapon = Weapon ()
        weapon.id =weaponData.id
        weapon.power = weaponData.power
        weapon.strength = weaponData.strength

        weaponIndex = 1

        if isinstance(self.rightHand, Weapon):
            logger.debug ('rightHand is Weapon')
            logger.debug ('weaponIndex: %s' % weaponIndex)
            self.leftHand = weapon
        else:
            if isinstance(self.leftHand, Weapon):
                weaponIndex = 2
                self.rightHand = weapon
                logger.debug ('leftHand is Weapon')
                logger.debug ('weaponIndex: %s' % weaponIndex)
            else:
                self.leftHand = weapon
                logger.debug ('leftHand is not Weapon')
                logger.debug ('weaponIndex: %s' % weaponIndex)

        return weaponIndex

     def hasWeapon (self):
         bool = False
         if isinstance(self.leftHand, Weapon) or isinstance(self.rightHand, Weapon):
             bool = True
         return bool



     def destroyEptitudes(self):
         self.eptitudes = []

     def hasSelfDieEptitude (self):
        flag = False
        for eptitude in self.eptitudes:
           if eptitude.getPeriod() == EptitudePeriod.SELF_DIE and eptitude.activate_widget:
                flag = True
        return flag


     def configureEptitudes (self, cardData):
         logger.debug('HeroUnit::configureEptitudes : %s' % len(cardData['eptitudes']))
         for eptitudeData in cardData['eptitudes']:
               eptitude = UnitEptitude ()
               eptitude.setType(eptitudeData['type'])
               eptitude.setPower(eptitudeData['power'])
               eptitude.max_power = eptitudeData['max_power']
               eptitude.count = eptitudeData['count']
               eptitude.setLevel(eptitudeData['level'])
               eptitude.setPeriod(eptitudeData['period'])
               eptitude.setLifecycle(eptitudeData['lifecycle'])
               eptitude.setAttachHero (eptitudeData['attach_hero'])
               eptitude.setAttachInitiator(eptitudeData['attach_initiator'])
               eptitude.setAttachment(eptitudeData['attachment'])
               eptitude.setDynamic(eptitudeData['dynamic'])
               eptitude.setCondition((eptitudeData['condition']))
               eptitude.spellCondition = eptitudeData['spellCondition']
               eptitude.id = eptitudeData['id']
               eptitude.battlecry = eptitudeData['battlecry']
               eptitude.dependency = eptitudeData['dependency']
               eptitude.attach_eptitude = eptitudeData['attach_eptitude']
               eptitude.price = eptitudeData['price']
               eptitude.probability = eptitudeData['probability']
               eptitude.spellSensibility = eptitudeData['spellSensibility']
               eptitude.activate_widget = eptitudeData['activate_widget']
               eptitude.animation = eptitudeData['animation']
               eptitude.manacost = eptitudeData['manacost']
               eptitude.widget = eptitudeData['widget']
               eptitude.destroy = eptitudeData['destroy']
               try:
                   eptitude.weapon(eptitudeData['weapon'])
               except: pass
               try:
                   eptitude.setRace(eptitudeData['race'])
               except: pass
               try:
                   eptitude.setSubrace(eptitudeData['subrace'])
               except: pass
               try:
                   eptitude.setUnit(eptitudeData['unit'])
               except: pass
               try:
                   eptitude.group = eptitudeData['group']
               except:
                   pass

               self.eptitudes.append (eptitude)



     def treatment (self, value):
        self.health += value
        if self.health > self.maxHealth:
            self.health = self.maxHealth

     def setHealth (self, health):
        self.health = health

     def getHealth (self):
        return self.health

     def getMaxHealth (self):
        return self.maxHealth

     def getAttack (self):
         return 0

     def getTitle (self):
         return 'hero'

     def getTotalAttack(self):
         return self.getAttack()

     def isProvocator(self):
         return False

     def getDefaultAttack (self):
        return self.defaultAttack

     def getWhiteFlag (self):
        return self.whiteFlag

     def hasEptitudeWithPeriod (self, period):
        flag = False
        logger.debug ('period: %s' % period)
        for eptitude in self.eptitudes:
            logger.debug ('getPeriod(): %s' % eptitude.getPeriod())
            logger.debug ('title: %s' % self.title)
            if eptitude.getPeriod() == period:
                flag = True
        return flag

     def getEptitudeById (self, id):
        resultEptitude = False
        for eptitude in self.eptitudes:
            if eptitude.id == id:
                resultEptitude = eptitude

        return resultEptitude

     def appendTempEptitude (self, eptitude):
         self.tempEptitudes.append(eptitude)

     def containsTempEptitudes (self):
         if len(self.tempEptitudes) > 0:
             return True
         else:
             return False



class Unit ():

    def __init__(self, cardData):
        self.index = 0
        self.cardData = cardData
        self.attack = cardData['attack']
        self.defaultAttack = self.attack
        self.dynamicAttack = 0
        self.extraAttack = 0
        self.health = cardData['health']
        self.defaultHealth = self.health
        self.maxHealth = self.health
        self.title = cardData['title']
        self.canAttack = True
        self.attackCount = 1
        self.jerk = False
        self.eptitudes = []
        self.provocation = False
        self.shield = False
        self.shadow = False

        self.totalStepAttack = 1
        self.stepAttack = 1
        self.stepAttackCount = 0
        self.stepCount = 0

        self.freeze = False
        self.freezeIndex = 0
        self.replaceFlag = False
        self.tempEptitudes = []
        self.dumbness = False
        self.spellInvisible = False
        self.spellUp = False
        self.fly = False

        try:
            race = Race.objects.get(title=cardData['race'])
            self.setRace(race)
        except Race.DoesNotExist:
            pass
        except KeyError:
            pass

        try:
            subrace = SubRace.objects.get(title=cardData['subrace'])
            self.setSubrace(subrace)
        except SubRace.DoesNotExist:
            pass
        except KeyError:
            pass

        logger.debug ('Unit constructor')

        for eptitudeData in cardData['eptitudes']:
            eptitude = self.getEpritudeByData(eptitudeData)
            self.eptitudes.append (eptitude)
            logger.debug('unit eptitude: %s' % eptitude.getData())

        #logger.debug ('attack: %s' % self.attack)
        #logger.debug ('health: %s' % self.health)

    def destroyBattlecryEptitudes(self):
        targets = []
        for eptitude in self.eptitudes:
            if eptitude.battlecry:
                targets.append(eptitude)
        for target in targets:
            index = self.eptitudes.index(target)
            del self.eptitudes[index]

    def destroyEptitude(self, eptitude):
        index = self.eptitudes.index(eptitude)
        del self.eptitudes[index]

    def getEpritudeByData (self ,eptitudeData):
        eptitude = UnitEptitude ()
        eptitude.setType(eptitudeData['type'])
        eptitude.setPower(eptitudeData['power'])
        eptitude.max_power = eptitudeData['max_power']
        eptitude.count = eptitudeData['count']
        eptitude.setLevel(eptitudeData['level'])
        eptitude.setPeriod(eptitudeData['period'])
        eptitude.setLifecycle(eptitudeData['lifecycle'])
        eptitude.setAttachHero (eptitudeData['attach_hero'])
        eptitude.setAttachInitiator(eptitudeData['attach_initiator'])
        eptitude.setAttachment(eptitudeData['attachment'])
        eptitude.setDynamic(eptitudeData['dynamic'])
        eptitude.setCondition(eptitudeData['condition'])
        eptitude.spellCondition = eptitudeData['spellCondition']
        eptitude.id = eptitudeData['id']
        eptitude.battlecry = eptitudeData['battlecry']
        eptitude.dependency = eptitudeData['dependency']
        eptitude.attach_eptitude = eptitudeData['attach_eptitude']
        eptitude.price = eptitudeData['price']
        eptitude.probability = eptitudeData['probability']
        eptitude.spellSensibility = eptitudeData['spellSensibility']
        eptitude.activate_widget = eptitudeData['activate_widget']
        eptitude.animation = eptitudeData['animation']
        eptitude.manacost = eptitudeData['manacost']
        eptitude.widget = eptitudeData['widget']
        eptitude.destroy = eptitudeData['destroy']
        try:
            eptitude.weapon = eptitudeData['weapon']
        except: pass
        try:
            eptitude.setRace(eptitudeData['race'])
        except: pass
        try:
            eptitude.setSubrace(eptitudeData['subrace'])
        except: pass
        try:
            eptitude.setUnit(eptitudeData['unit'])
        except: pass
        try:
            eptitude.group = eptitudeData['group']
        except:
            pass
        return eptitude

    def attachEptitude (self, eptitude):
        eptitude.attached = True
        self.eptitudes.append (eptitude)
        logger.debug('attached eptitude: %s' % eptitude.getData())

    def containsTempEptitudes(self):
        if len(self.tempEptitudes):
            return True
        return False

    def treatment (self, value):
        self.health += value
        if self.health > self.maxHealth:
            self.health = self.maxHealth

    def getDefaultAttack (self):
        return self.defaultAttack


    def setIndex (self, value):
        self.index = value

    def setRow (self, value):
        self.row = value

    def setWhiteFlag (self, value):
        self.whiteFlag = value

    def getWhiteFlag (self):
        return self.whiteFlag

    def getTitle (self):
        return self.title

    def setAttack(self, attack):
        self.attack = attack

    def getAttack (self):
        return self.attack

    def setDynamicAttack (self, attack):
        self.dynamicAttack = attack

    def getDynamicAttack (self):
        return self.dynamicAttack

    def setHealth (self, health):
        self.health = health

    def getHealth (self):
        return self.health

    def setMaxHealth (self, health):
        self.maxHealth = health

    def getMaxHealth (self):
        return self.maxHealth

    def setStepAttack (self, attack):
        self.stepAttack = attack


    def isProvocator(self):
        return self.provocation

    def getCardData (self):
        return self.cardData

    def getTotalAttack (self):
        return self.attack + self.dynamicAttack + self.extraAttack

    def setRace(self, value):
        self.race = value

    def setSubrace (self, value):
        self.subrace = value

    def hasEptitudeWithPeriod (self, period):
        flag = False
        logger.debug ('period: %s' % period)
        for eptitude in self.eptitudes:
            logger.debug ('getPeriod(): %s' % eptitude.getPeriod())
            logger.debug ('title: %s' % self.title)
            if eptitude.getPeriod() == period:
                flag = True
        return flag

    def hasActiveEptitude(self):
        flag = False
        for eptitude in self.eptitudes:
            if eptitude.getPeriod() == EptitudePeriod.ACTIVATE_ACTIVE:
                flag = True
        return flag


    def hasSelfDieEptitude (self):
        flag = False
        for eptitude in self.eptitudes:
           if eptitude.getPeriod() == EptitudePeriod.SELF_DIE and eptitude.activate_widget:
                flag = True
        return flag

    def getEptitudeById (self, id):
        resultEptitude = False
        for eptitude in self.eptitudes:
            if eptitude.id == id:
                resultEptitude = eptitude

        return resultEptitude



class UnitEptitude ():

    def __init__(self):
        self.condition = 0
        self.activated = False
        self.id = -1
        self.dependency = 0
        self.attach_eptitude = 0
        self.battlecry = False
        self.price = -1
        self.probability = 100
        self.spellSensibility = False
        self.spellCondition = 0
        self.count = 0
        self.attached = False
        self.max_power = 0
        self.target = None
        self.activate_widget = False
        self.animation = -1
        self.manacost = 0
        self.widget = 0
        self.destroy = False



    def clone(self):
        eptitude = UnitEptitude()
        eptitude.condition = self.condition
        eptitude.spellCondition = self.spellCondition
        eptitude.activated = self.activated
        eptitude.id = self.id
        eptitude.dependency = self.dependency
        eptitude.attach_eptitude = self.attach_eptitude
        eptitude.battlecry = self.battlecry
        eptitude.probability = self.probability
        eptitude.spellSensibility = self.spellSensibility
        eptitude.attached = self.attached
        eptitude.activate_widget = self.activate_widget
        eptitude.animation = self.animation
        eptitude.manacost = self.manacost
        eptitude.widget = self.widget
        eptitude.destroy = self.destroy
        try:
            eptitude.target = self.target
        except:
            pass

        try:
            eptitude.period = self.period
        except:
            pass
        try:
            eptitude.level = self.level
        except:
            pass
        try:
            eptitude.type = self.type
        except:
            pass
        try:
            eptitude.race = self.race
        except:
            pass
        try:
            eptitude.weapon = self.weapon
        except:
            pass
        try:
            eptitude.subrace = self.subrace
        except:
            pass
        try:
            eptitude.unit = self.unit
        except:
            pass
        try:
            eptitude.power = self.power
        except:
            pass
        eptitude.max_power = self.power

        try:
            eptitude.count = self.count
        except:
            pass
        try:
            eptitude.lifecycle = self.lifecycle
        except:
            pass
        try:
            eptitude.attachment = self.attachment
        except:
            pass
        try:
            eptitude.attachHero = self.attachHero
        except:
            pass
        try:
            eptitude.attachInitiator = self.attachInitiator
        except:
            pass
        try:
            eptitude.dynamic = self.dynamic
        except:
            pass
        try:
            eptitude.condition = self.condition
        except:
            pass
        return eptitude

    def setPeriod (self, value):
        self.period = value
    def getPeriod (self):
        return self.period

    def setLevel (self, value):
        self.level = value
    def getLevel (self):
        return self.level

    def setType (self, value):
        self.type = value
    def getType(self):
        return self.type

    def setRace(self, value):
        self.race = value

    def getRace(self):
        return self.race

    def setSubrace(self, value):
        self.subrace = value

    def getSubrace (self):
        return self.subrace

    def setUnit (self, value):
        self.unit = value

    def getUnit(self):
        return self.unit

    def setPower(self, value):
        self.power = value
    def getPower(self):
        return self.power

    def setLifecycle(self, value):
        self.lifecycle = value
    def getLifecycle(self):
        return self.lifecycle

    def setAttachment(self, value):
        self.attachment = value
    def getAttachment(self):
        return self.attachment

    def setAttachHero(self, value):
        self.attachHero = value
    def getAttachHero(self):
        return attachHero

    def setAttachInitiator(self, value):
        self.attachInitiator = value
    def getAttachInitator(self):
        return self.attachInitiator

    def setDynamic (self, value):
        self.dynamic = value

    def setCondition (self, value):
        self.condition = value

    def getCondition (self):
        return self.condition


    def getData(self):
        self.data = {}
        try:
            self.data['level'] = self.level
        except: pass
        try:
            self.data['period'] = self.period
        except: pass
        try:
            self.data['type'] = self.type
        except: pass
        try:
            self.data['power'] = self.power
        except: pass
        try:
            self.data['lifecycle'] = self.lifecycle
        except: pass

        self.data['attachment'] = self.attachment
        self.data['attachHero'] = self.attachHero

        try:
            self.data['attachInitiator'] = self.attachInitiator
        except: pass
        try:
            self.data['subrace'] = self.subrace
        except: pass
        try:
            self.data['race'] = self.race
        except: pass
        try:
            self.data['unit'] = self.unit
        except: pass
        try:
            self.data['dynamic'] = self.dynamic
        except: pass
        try:
            self.data['condition'] = self.condition
        except: pass
        self.data['animation'] = self.animation
        try:
            self.data['manacost'] = self.manacost
        except: pass
        self.data['widget'] = self.widget

        return self.data

