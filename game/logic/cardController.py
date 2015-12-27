__author__ = 'RIK'

import logging
logger = logging.getLogger('game_handler')

import random

from game.logic.constants import EptitudePeriod, EptitudeCondition, EptitudeLevel, EptitudeAttachment, EptitudeType
from game.logic.action import Action


class CardController ():

    def __init__(self, controller=None):
        self.id = random.randint(0, 10000)
        if controller:
            self.setMatch(controller.match)
            self.setScenario(controller.scenario)
            self.setClient(controller.client)
            self.setWhiteFlag(controller.whiteFlag)

    def setScenario(self, scenario):
        self.scenario = scenario
        return self

    def setMatch(self, match):
        self.match = match
        return self

    def setClient(self, client):
        self.client = client
        return self

    def setWhiteFlag(self, flag):
        self.whiteFlag = flag
        return self

    def activate_both_hands(self, eptitude_period):
        """Активировать все карты в руках определенным периодом"""
        for card in self.match.white_hand:
            self.activate(card, eptitude_period)

        for card in self.match.black_hand:
            self.activate(card, eptitude_period)

    def new_card(self):
        self.activate_both_hands(EptitudePeriod.CARD_MODE_NEW_CARD)

        if self.match.whiteHeroUnit.getHealth() < self.match.whiteHeroUnit.defaultHealth:
            self.hero_wound(True)

        if self.match.blackHeroUnit.getHealth() < self.match.blackHeroUnit.defaultHealth:
            self.hero_wound(False)

        self.new_unit()

    def new_unit(self):
        self.activate_both_hands(EptitudePeriod.CARD_MODE_NEW_UNIT)

    def unit_die(self, whiteFlag):
        self.activate_both_hands(EptitudePeriod.CARD_MODE_UNIT_DIE)

    def freeze(self):
        self.activate_both_hands(EptitudePeriod.CARD_MODE_FREEZE)

    def destroy_shield(self):
        self.activate_both_hands(EptitudePeriod.CARD_MODE_DESTROY_SHIELD)

    def play_card(self):
        self.activate_both_hands(EptitudePeriod.CARD_MODE_PLAY_CARD)

    def hero_wound(self, hero_white_flag):
        for card in self.match.white_hand + self.match.black_hand:
            if heroWhiteFlag == card['whiteFlag']:
                self.activate(card, EptitudePeriod.CARD_MODE_PLAYER_HERO_WOUND)
            else:
                self.activate(card, EptitudePeriod.CARD_MODE_OPPONENT_HERO_WOUND)

    def activate(self, card, period):
        card = card
        eptitudes = card['eptitudes'][:]
        while len(eptitudes):
            eptitude = eptitudes[0]
            del self.eptitudes[0]

            if period == eptitude['period']:

                if eptitude['type'] == EptitudeType.DECREASE_PRICE_DEPENDS_ON_TOKENS:
                    logger.debug(
                        'CardController activate: eptitude.type: DECREASE_PRICE_DEPENDS_ON_TOKENS')
                    self.decrease_price_depends_on_tokens(card)

                if eptitude['type'] == EptitudeType.DECREASE_PRICE_DEPENDS_ON_RACE_TOKENS:
                    logger.debug(
                        'CardController activate: eptitude.type: DECREASE_PRICE_DEPENDS_ON_RACE_TOKENS')
                    self.decrease_price_depends_on_race_tokens(card, eptitude)

                if eptitude['type'] == EptitudeType.DECREASE_PRICE_DEPENDS_ON_SHIELD_TOKENS:
                    logger.debug(
                        'CardController activate: eptitude.type: DECREASE_PRICE_DEPENDS_ON_SHIELD_TOKENS')
                    self.decrease_price_depends_on_shield_tokens(card, eptitude)

                if eptitude['type'] == EptitudeType.DECREASE_PRICE_DEPENDS_ON_PLAYER_CARDS:
                    logger.debug(
                        'CardController activate: eptitude.type: DECREASE_PRICE_DEPENDS_ON_PLAYER_CARDS')
                    self.decrease_price_depends_on_player_cards(card)

                if eptitude['type'] == EptitudeType.DECREASE_PRICE_DEPENDS_ON_OPPONENT_CARDS:
                    logger.debug(
                        'CardController activate: eptitude.type: DECREASE_PRICE_DEPENDS_ON_OPPONENT_CARDS')
                    self.decrease_price_depends_on_opponent_cards(card)

                if eptitude['type'] == EptitudeType.DECREASE_PRICE_DEPENDS_ON_HERO_HEALTH:
                    logger.debug(
                        'CardController activate: eptitude.type: DECREASE_PRICE_DEPENDS_ON_HERO_HEALTH')
                    self.decrease_price_depends_on_hero_health(card)

                if eptitude['type'] == EptitudeType.DECREASE_PRICE_DEPENDS_ON_DIE_UNITS:
                    logger.debug(
                        'CardController activate: eptitude.type: DECREASE_PRICE_DEPENDS_ON_DIE_UNITS')
                    self.decrease_price_depends_on_die_units(card, eptitude)

                if eptitude['type'] == EptitudeType.DECREASE_PRICE_DEPENDS_ON_FROZEN_TOKENS:
                    logger.debug(
                        'CardController activate: eptitude.type: DECREASE_PRICE_DEPENDS_ON_DIE_UNITS')
                    self.decrease_price_depends_on_freeze_tokens(card, eptitude)

    def decrease_price(self, card, value, attachment, index):
        """Вспомогательная функция для функций decrease_price_depends_on_*"""
        # меняем цену в самой карте
        if value > card['defaultPrice']:
            value = card['defaultPrice']
        card['price'] = card['defaultPrice'] - value

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

    def decrease_price_depends_on_player_cards(self, card):
        attachment, index = self.match.initCardAttachment(card, self.whiteFlag)
        if card['whiteFlag']:
            value = len(self.match.white_hand)
        else:
            value = len(self.match.black_hand)

        self.decrease_price(card, value, attachment, index)

    def decrease_price_depends_on_opponent_cards(self, card):
        attachment, index = self.match.initCardAttachment(card, self.whiteFlag)

        if card['whiteFlag']:
            value = len(self.match.black_hand)
        else:
            value = len(self.match.white_hand)

        self.decrease_price(card, value, attachment, index)

    def decrease_price_depends_on_tokens(self, card):
        attachment, index = self.match.initCardAttachment(card, self.whiteFlag)

        value = len(self.match.whiteUnitRow) + len(self.match.blackUnitRow)

        self.decrease_price(card, value, attachment, index)

    def decrease_price_depends_on_hero_health(self, card):
        attachment, index = self.match.initCardAttachment(card, self.whiteFlag)

        if card['whiteFlag']:
            hero = self.match.whiteHeroUnit
        else:
            hero = self.match.blackHeroUnit

        value = hero.defaultHealth - hero.getHealth()

        self.decrease_price(card, value, attachment, index)

    def decrease_price_depends_on_race_tokens(self, card, eptitude):
        attachment, index = self.match.initCardAttachment(card, self.whiteFlag)

        value = 0
        for unit in self.match.whiteUnitRow:
            if unit.race.id == eptitude['race']:
                value += 1

        for unit in self.match.blackUnitRow:
            if unit.race.id == eptitude['race']:
                value += 1

        value *= eptitude['power']

        self.decrease_price(card, value, attachment, index)

    def decrease_price_depends_on_shield_tokens(self, card, eptitude):
        attachment, index = self.match.initCardAttachment(card, self.whiteFlag)

        value = 0
        for unit in self.match.whiteUnitRow:
            if unit.shield:
                value += 1

        for unit in self.match.blackUnitRow:
            if unit.shield:
                value += 1

        value *= eptitude['power']

        self.decrease_price(card, value, attachment, index)

    def decrease_price_depends_on_freeze_tokens(self, card, eptitude):
        attachment, index = self.match.initCardAttachment(card, self.whiteFlag)

        value = 0
        for unit in self.match.whiteUnitRow:
            if unit.freeze:
                value += 1

        for unit in self.match.blackUnitRow:
            if unit.freeze:
                value += 1

        if self.match.whiteHeroUnit.freeze:
            value += 1

        if self.match.blackHeroUnit.freeze:
            value += 1

        value *= eptitude['power']

        self.decrease_price(card, value, attachment, index)

    def decrease_price_depends_on_die_units(self, card, eptitude):
        attachment, index = self.match.initCardAttachment(card, self.whiteFlag)

        value = self.match.dieUnitsIndex
        value *= eptitude['power']

        self.decrease_price(card, value, attachment, index)
