__author__ = 'inozemcev'

import tornado.web as web
import tornado.websocket as websocket
import json;
import redis
import random

from game.logic.la import Game

import logging
logger =  logging.getLogger('game_handler')

class MatchHandler(websocket.WebSocketHandler):
    matches = {}

    def check_origin(self, origin):
        return True

    def open(self, match_id):
        logger.debug('MatchHandler::Open match_id:%s' % match_id)

        redis_client = redis.StrictRedis()
        match = 'la_game_match:%s' % match_id

        cached_game_id =(redis_client.hget(match, 'id'))

        if cached_game_id == None:
            response = {}
            response['status'] = 'success'
            response['type'] = 'match_doesnt_exist'
            dump = json.dumps(response)
            self.write_message (dump)
            return 

        if not match_id in MatchHandler.matches:
            game = MatchHandler.matches[match_id] = Game(int(match_id))

            game.setPlayer1_id(redis_client.hget(match, 'player1'))
            game.setPlayer2_id(redis_client.hget(match, 'player2'))

            game.setPlayer1_level(redis_client.hget(match, 'player1_level'))
            game.setPlayer2_level(redis_client.hget(match, 'player2_level'))

            game.setPlayer1_deck(redis_client.hget(match, 'player1_deckId'))
            game.setPlayer2_deck(redis_client.hget(match, 'player2_deckId'))

            game.setPlayer1_hero(redis_client.hget(match, 'player1_heroId'))
            game.setPlayer2_hero(redis_client.hget(match, 'player2_heroId'))

            game.setMode (redis_client.hget(match, 'match_type'))
            logger.debug('match type: %s' % game.getMode())

        self.match = MatchHandler.matches[match_id]

    def on_close(self):
        logger.debug('MatchHandler::Close id:%s' % self.id)

        # если оба игрока отсоединились удалить матч

    def handle_request(self, response):
        logger.debug('MatchHandler::handle_request')

    def isWhite(self):
        return self.id == self.match.getWhiteId()


    def on_message(self, message):

        #logger.debug('MatchHandler::onmessage')
        event = json.loads(message)

        type = event['type']

        if not hasattr(self, 'id'):
            self.id = int(event['id'])

        if type == 'connect_to_match':
            logger.debug ('connect_to_match')

            self.player1_id = self.match.getPlayer1_id()
            self.player2_id = self.match.getPlayer2_id()

            if int(self.id) == int(self.player1_id):
                self.match.setPlayer1(self)

            if int(self.id) == int(self.player2_id):
                self.match.setPlayer2(self)

            if not self.match.allPlayersInit():
                return

            #self.match.launchTimers()


            if bool(random.getrandbits(1)):
                self.match.setWhite(self.match.getPlayer1())
                self.match.setBlack(self.match.getPlayer2())
                self.match.setWhiteDeck (self.match.getPlayer1_deck())
                self.match.setBlackDeck (self.match.getPlayer2_deck())

                self.match.setWhiteId(self.player1_id)
                self.match.setBlackId(self.player2_id)

                self.match.setWhiteHero (self.match.getPlayer1_hero())
                self.match.setBlackHero (self.match.getPlayer2_hero())

                self.match.setWhiteHeroLevel (self.match.getPlayer1_level())
                self.match.setBlackHeroLevel (self.match.getPlayer2_level())

            else:
                self.match.setBlack(self.match.getPlayer1())
                self.match.setWhite(self.match.getPlayer2())
                self.match.setWhiteDeck (self.match.getPlayer2_deck())
                self.match.setBlackDeck (self.match.getPlayer1_deck())

                self.match.setWhiteId(self.player2_id)
                self.match.setBlackId(self.player1_id)

                self.match.setWhiteHero (self.match.getPlayer2_hero())
                self.match.setBlackHero (self.match.getPlayer1_hero())

                self.match.setWhiteHeroLevel (self.match.getPlayer2_level())
                self.match.setBlackHeroLevel (self.match.getPlayer1_level())

            self.match.generateMatchDecks()
            self.match.initializeAchieves()

            self.match.runPreflopTimer()

            self.match.generateHand (3, True)
            self.match.generateHand (4, False)

            self.match.generateHeroesHealth()
            self.match.generateHeroesUnits()

            self.response = {}
            self.response['status'] = 'success'
            self.response['type'] = 'preflop'
            self.data = {}
            self.data['preflop'] = self.match.getWhiteHand()
            self.data['opponent_preflop'] = self.match.getBlackHand()

            self.data['achieves'] = self.match.getWhiteAchieves()
            self.data['opponent_achieves'] = self.match.getBlackAchieves()

            self.data['hero'] = self.match.getWhiteHero().hero.uid
            self.data['opponent_hero'] = self.match.getBlackHero().hero.uid
            self.data['level'] = self.match.getWhiteHeroLevel()
            self.data['opponent_level'] = self.match.getBlackHeroLevel()
            self.data['health'] = self.match.getWhiteHeroHealth()
            self.data['opponent_health'] = self.match.getBlackHeroHealth()

            self.data['mode'] = self.match.getMode()



            self.data['white'] = True
            self.response['data'] = self.data
            self.dump = json.dumps(self.response)
            self.match.getWhite().write_message (self.dump)

            self.response = {}
            self.response['status'] = 'success'
            self.response['type'] = 'preflop'
            self.data = {}
            self.data['preflop'] = self.match.getBlackHand()
            self.data['opponent_preflop'] = self.match.getWhiteHand()

            self.data['achieves'] = self.match.getBlackAchieves()
            self.data['opponent_achieves'] = self.match.getWhiteAchieves()

            self.data['hero'] = self.match.getBlackHero().hero.uid
            self.data['opponent_hero'] = self.match.getWhiteHero().hero.uid
            self.data['level'] = self.match.getBlackHeroLevel()
            self.data['opponent_level'] = self.match.getWhiteHeroLevel()
            self.data['health'] = self.match.getBlackHeroHealth()
            self.data['opponent_health'] = self.match.getWhiteHeroHealth()

            self.data['mode'] = self.match.getMode()
            self.data['white'] = False
            self.response['data'] = self.data
            self.dump = json.dumps(self.response)
            self.match.getBlack().write_message(self.dump)

        if type == 'change_preflop':
            logger.debug('change_preflop')

            self.response = {}
            self.response['status'] = 'success'
            self.response['type'] = 'change_preflop'
            self.data = {}

            if self.id == self.match.getWhiteId():
                self.preflop = self.match.changePreflop (event['data']['preflop'], True)
                self.data['preflop'] = self.preflop
                self.opponent = self.match.getBlack()

            if self.id == self.match.getBlackId():
                self.preflop =  self.match.changePreflop (event['data']['preflop'], False)
                self.data['preflop'] = self.preflop
                self.opponent = self.match.getWhite()

            self.response['data'] = self.data
            self.dump = json.dumps(self.response)
            self.write_message(self.dump)

            self.response['type'] = 'change_opponent_preflop'
            self.data['opponent_preflop'] = event['data']['preflop']
            self.response['data'] = self.data
            self.dump = json.dumps(self.response)
            self.opponent.write_message (self.dump)



        if type == 'end_change_preflop':
            if self.match.isAllPlayersChangePreflop():

                logger.debug('end_change_preflop')
                if self.match.blockEndPreflop:
                    return

                self.match.blockEndPreflop = True
                
                self.match.stopPreflopTimer()

                response = {}
                response['status'] = 'success'
                response['type'] = 'end_preflop'

                data = {}
                data['preflop'] = self.match.getWhiteHand()
                data['mode'] = self.match.getMode()
                if self.match.getMode() == 2:
                    data['deck'] = self.match.getDeckData(True)
                response['data'] = data
                dump = json.dumps(response)
                self.match.getWhite().write_message(dump)

                data = {}
                data['preflop'] = self.match.getBlackHand()
                data['mode'] = self.match.getMode()
                if self.match.getMode() == 2:
                    data['deck'] = self.match.getDeckData(False)
                response['data'] = data
                dump = json.dumps(response)
                self.match.getBlack().write_message(dump)

        if type == 'preflop_click':

                response = {}
                response['status'] = 'success'
                response['type'] = 'opponent_preflop_click'
                response['data'] = event['data']
                dump = json.dumps(response)

                if self.id == self.match.getWhiteId():
                    self.match.getBlack().write_message(dump)
                else:
                    self.match.getWhite().write_message(dump)

        if type == 'ready':

                if self.id == self.match.getWhiteId():
                    self.match.whiteReady()
                else:
                    self.match.blackReady()

                if self.match.isReady():

                    scenario = self.match.start()

                    response = {}
                    response['status'] = 'success'
                    response['type'] = 'scenario'
                    data = {}
                    data['scenario'] = scenario
                    response['data'] = data
                    dump = json.dumps(response)

                    self.match.getWhite().write_message(dump)
                    self.match.getBlack().write_message(dump)

        if type == 'activate_achieve':
                    logger.debug ('activate_achieve')
                    position =  event['data']['position']
                    whiteFlag = self.isWhite()

                    self.match.activateAchieve(position, whiteFlag)

                    response = {}
                    response['status'] = 'success'
                    response['type'] = 'scenario'
                    data = {}
                    data['scenario'] = self.match.getScenario()
                    response['data'] = data
                    dump = json.dumps(response)

                    self.match.getWhite().write_message(dump)
                    self.match.getBlack().write_message(dump)

        if type == 'activate_achieve_to_target':
                    logger.debug ('activate_achieve_to_target')
                    position =  event['data']['position']
                    whiteFlag = self.isWhite()
                    targetAttachment = event['data']['attachment']
                    targetIndex = event['data']['targetIndex']

                    self.match.activateAchieveToTarget(targetIndex, targetAttachment, position, whiteFlag)

                    response = {}
                    response['status'] = 'success'
                    response['type'] = 'scenario'
                    data = {}
                    data['scenario'] = self.match.getScenario()
                    response['data'] = data
                    dump = json.dumps(response)

                    self.match.getWhite().write_message(dump)
                    self.match.getBlack().write_message(dump)


        if type == 'play_card':
                    logger.debug ('play_card')

                    index =  event['data']['index']
                    position = event['data']['position']
                    whiteFlag = self.isWhite()

                    cardType = int(event['data']['cardType'])

                    # если карта юнит
                    if cardType == 0:
                        self.match.playSpell(index, whiteFlag)

                    if cardType == 2:
                       self.match.addUnit(index, position, whiteFlag)

                    response = {}
                    response['status'] = 'success'
                    response['type'] = 'scenario'
                    data = {}
                    data['scenario'] = self.match.getScenario()
                    response['data'] = data
                    dump = json.dumps(response)

                    self.match.getWhite().write_message(dump)
                    self.match.getBlack().write_message(dump)

        if type == 'play_card_spell_to_target':
                    logger.debug ('play_card_spell_to_target')

                    cardIndex =  event['data']['cardIndex']
                    logger.debug('cardIndex:%s' % cardIndex)

                    targetAttachment = event['data']['attachment']
                    logger.debug('targetAttachment:%s' % targetAttachment)

                    targetIndex = event['data']['targetIndex']
                    logger.debug('targetIndex:%s' % targetIndex)

                    whiteFlag = self.isWhite()


                    self.match.spellToTarget(cardIndex, targetIndex, targetAttachment, whiteFlag)

                    response = {}
                    response['status'] = 'success'
                    response['type'] = 'scenario'
                    data = {}
                    data['scenario'] = self.match.getScenario()
                    response['data'] = data
                    dump = json.dumps(response)

                    self.match.getWhite().write_message(dump)
                    self.match.getBlack().write_message(dump)

        if type == 'spell_to_target_for_effect':
                    logger.debug ('spell_to_target_for_effect')

                    targetAttachment = event['data']['attachment']
                    logger.debug('targetAttachment:%s' % targetAttachment)

                    targetIndex = event['data']['targetIndex']
                    logger.debug('targetIndex:%s' % targetIndex)

                    whiteFlag = self.isWhite()

                    self.match.spellToTargetForEffect(targetIndex, targetAttachment, whiteFlag)

                    response = {}
                    response['status'] = 'success'
                    response['type'] = 'scenario'
                    data = {}
                    data['scenario'] = self.match.getScenario()
                    response['data'] = data
                    dump = json.dumps(response)

                    self.match.getWhite().write_message(dump)
                    self.match.getBlack().write_message(dump)



        if type == 'end_step':
                    logger.debug ('end_step')

                    scenario = self.match.endStep()
                    response = {}
                    response['status'] = 'success'
                    response['type'] = 'scenario'
                    data = {}
                    data['scenario'] = scenario
                    response['data'] = data
                    dump = json.dumps(response)
                    self.match.getWhite().write_message(dump)
                    self.match.getBlack().write_message(dump)


        if type == 'classic_attack':
                    logger.debug ('classic_attack')
                    if self.id == self.match.getWhiteId():
                         self.whiteFlag = True
                    else:
                         self.whiteFlag = False

                    initiatorIndex =  event['data']['initiatorIndex']
                    logger.debug ('initiatorIndex:%s' % initiatorIndex)

                    targetIndex =  event['data']['targetIndex']
                    logger.debug ('targetIndex:%s' % targetIndex)

                    scenario = self.match.classicAttack (initiatorIndex, targetIndex, self.whiteFlag)

                    response = {}
                    response['status'] = 'success'
                    response['type'] = 'scenario'
                    data = {}
                    data['scenario'] = scenario
                    response['data'] = data
                    dump = json.dumps(response)

                    self.match.getWhite().write_message(dump)
                    self.match.getBlack().write_message(dump)

        if type == 'init_select':
                    if self.id == self.match.getWhiteId():
                         self.whiteFlag = True
                    else:
                         self.whiteFlag = False

                    selectData = event['data']['serviceData']

                    scenario = self.match.continueAddUnit (selectData, self.whiteFlag)

                    response = {}
                    response['status'] = 'success'
                    response['type'] = 'scenario'
                    data = {}
                    data['scenario'] = scenario
                    response['data'] = data
                    dump = json.dumps(response)

                    self.match.getWhite().write_message(dump)
                    self.match.getBlack().write_message(dump)

        if type == 'cancel_select':

                    if self.id == self.match.getWhiteId():
                         self.whiteFlag = True
                    else:
                         self.whiteFlag = False

                    scenario = self.match.cancelSelect (self.whiteFlag)

                    response = {}
                    response['status'] = 'success'
                    response['type'] = 'scenario'
                    data = {}
                    data['scenario'] = scenario
                    response['data'] = data
                    dump = json.dumps(response)
                    self.write_message (dump)

        if type == 'replace_deck_items':
                    if self.id == self.match.getWhiteId():
                         whiteFlag = True
                    else:
                         whiteFlag = False
                    logger.debug('replace_deck_items')
                    initiator = event['data']['initiator']
                    target = event['data']['target']
                    self.match.replaceDeckItems(initiator, target, whiteFlag)
                    response = {}
                    response['status'] = 'success'
                    response['type'] = 'replace_deck_items'
                    data = {}
                    data['initiator'] = initiator
                    data['target'] = target
                    response['data'] = data
                    dump = json.dumps(response)
                    self.write_message (dump)




        if type == 'effect_selected':
                    if self.id == self.match.getWhiteId():
                         self.whiteFlag = True
                    else:
                         self.whiteFlag = False

                    index = int(event['data']['index'])
                    scenario = self.match.effect_selected (self.whiteFlag, index)

                    response = {}
                    response['status'] = 'success'
                    response['type'] = 'scenario'
                    data = {}
                    data['scenario'] = scenario
                    response['data'] = data
                    dump = json.dumps(response)

                    self.match.getWhite().write_message(dump)
                    self.match.getBlack().write_message(dump)

        if type == 'guise_selected':
                    if self.id == self.match.getWhiteId():
                         self.whiteFlag = True
                    else:
                         self.whiteFlag = False

                    index = int(event['data']['index'])
                    scenario = self.match.guise_selected (self.whiteFlag, index)

                    response = {}
                    response['status'] = 'success'
                    response['type'] = 'scenario'
                    data = {}
                    data['scenario'] = scenario
                    response['data'] = data
                    dump = json.dumps(response)

                    self.match.getWhite().write_message(dump)
                    self.match.getBlack().write_message(dump)

        if type == 'end_match':
            logger.debug('MatchHandler::end_match')
            '''
            if self.id == self.match.getWhiteId():
                self.client = self.match.getWhite()
            else:
                self.client = self.match.getBlack()
            '''

            response = {}
            response['status'] = 'success'
            response['type'] = 'end_match'
            response['data'] = {}
            dump = json.dumps(response)
            self.write_message(dump)
            #self.close()










































