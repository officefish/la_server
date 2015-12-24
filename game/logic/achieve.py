__author__ = 'RIK'
from game.logic.unit import UnitEptitude


class UAchieve ():

    def __init__(self, achieveModel, whiteFlag):
        self.title = achieveModel.achieve.title
        self.description = achieveModel.achieve.description
        self.autonomic = achieveModel.achieve.autonomic
        self.price = achieveModel.achieve.price
        self.type = achieveModel.achieve.type
        self.position = achieveModel.position
        self.incrementIndex = 0
        self.whiteFlag = whiteFlag

        self.eptitudes = []

        for eptitudeModel in achieveModel.achieve.eptitudes:
            eptitude = UnitEptitude()
            eptitude.setType(eptitudeModel.type)
            eptitude.setLevel(eptitudeModel.level)
            eptitude.setPeriod(eptitudeModel.period)

            eptitude.setPower(eptitudeModel.power)
            eptitude.max_power = eptitudeModel.max_power
            eptitude.count = eptitudeModel.count

            eptitude.setLifecycle(eptitudeModel.level)
            eptitude.setAttachHero(eptitudeModel.attach_hero)
            eptitude.setAttachInitiator(eptitudeModel.attach_initiator)
            eptitude.setAttachment(eptitudeModel.attachment)
            self.attachment = eptitudeModel.attachment
            self.attach_hero = eptitudeModel.attach_hero

            eptitude.setDynamic(eptitudeModel.dynamic)
            eptitude.setCondition(eptitudeModel.condition)
            eptitude.spellCondition = eptitudeModel.spellCondition
            eptitude.id = eptitudeModel.id
            eptitude.battlecry = eptitudeModel.battlecry
            eptitude.dependency = eptitudeModel.dependency
            eptitude.attach_eptitude = eptitudeModel.attach_eptitude
            eptitude.price = eptitudeModel.price
            eptitude.probability = eptitudeModel.probability
            eptitude.spellSensibility = eptitudeModel.spellSensibility
            try:
                eptitude.setRace(eptitudeModel.race.id)
            except:
                pass
            try:
                eptitude.setSubrace(eptitudeModel.subrace.id)
            except:
                pass
            try:
                eptitude.setUnit(eptitudeModel.unit.id)
            except:
                pass
            try:
                eptitude.group = eptitudeModel.group.id
            except:
                pass

            self.eptitudes.append(eptitude)

    def getData(self):
        data = {}
        data['title'] = self.title
        data['description'] = self.description
        data['price'] = self.price
        data['autonomic'] = self.autonomic
        data['type'] = self.type
        data['attachment'] = self.attachment
        data['attach_hero'] = self.attach_hero
        return data

    def getWhiteFlag(self):
        return self.whiteFlag

    def increment(self):
        if self.incrementIndex < self.price:
            self.incrementIndex += 1
        return self.incrementIndex

    def maxIncrement(self):
        return self.incrementIndex == self.price
