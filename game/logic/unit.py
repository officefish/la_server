__author__ = 'RIK'
import logging
logger =  logging.getLogger('game_handler')

class HeroUnit ():
     def __init__(self, health):
        self.health = health

     def setHealth (self, health):
        self.health = health

     def getHealth (self):
        return self.health

     def getAttack (self):
         return 0

     def getTitle (self):
         return 'hero'

     def isProvocator(self):
         return False


class Unit ():

    def __init__(self, cardData):
        self.index = 0
        self.cardData = cardData
        self.attack = cardData['attack']
        self.dynamicAttack = 0
        self.health = cardData['health']
        self.maxHealth = self.health
        self.title = cardData['title']
        self.canAttack = True
        self.attackCount = 1
        self.jerk = False
        self.eptitudes = []
        self.provocation = False

        logger.debug ('Unit constructor')

        for eptitudeData in cardData['eptitudes']:
            eptitude = UnitEptitude ()
            eptitude.setType(eptitudeData['type'])
            eptitude.setPower(eptitudeData['power'])
            eptitude.setLevel(eptitudeData['level'])
            eptitude.setPeriod(eptitudeData['period'])
            eptitude.setLifecycle(eptitudeData['lifecycle'])
            eptitude.setAttachHero (eptitudeData['attach_hero'])
            eptitude.setAttachInitiator(eptitudeData['attach_initiator'])
            eptitude.setAttachment(eptitudeData['attachment'])
            try:
                eptitude.setRace(eptitudeData['race'])
            except: pass
            try:
                eptitude.setSubrace(eptitudeData['subrace'])
            except: pass
            try:
                eptitude.setUnit(eptitudeData['unit'])
            except: pass

            self.eptitudes.append (eptitude)
            logger.debug('unit eptitude: %s' % eptitude.getData())

        #logger.debug ('attack: %s' % self.attack)
        #logger.debug ('health: %s' % self.health)


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
        return self.attack + self.dynamicAttack

class UnitEptitude ():

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
    def getAttachHero(self, value):
        return attachHero

    def setAttachInitiator(self, value):
        self.attachInitiator = value
    def getAttachInitator(self):
        return self.attachInitiator


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
        try:
            self.data['attachment'] = self.attachment
        except: pass
        try:
            self.data['attachHero'] = self.attachHero
        except: pass
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


        return self.data