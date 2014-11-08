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

        redis_client = redis.StrictRedis ();
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
            logger.debug('init Game')

        self.match = MatchHandler.matches[match_id]

    def on_close(self):
        logger.debug('MatchHandler::Close')

    def handle_request(self, response):
        logger.debug('MatchHandler::handle_request')


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
                self.white_opponent_id = self.player2_id
                self.black_opponent_id = self.player1_id

            else:
                self.match.setBlack(self.match.getPlayer1())
                self.match.setWhite(self.match.getPlayer2())
                self.white_opponent_id = self.player1_id
                self.black_opponent_id = self.player2_id

            self.match.generateMatchDecks()

            self.response = {}
            self.response['status'] = 'success'
            self.response['type'] = 'preflop'
            self.data = {}
            self.data['preflop'] = self.match.getPreflop (3, 1)
            self.response['data'] = self.data
            self.dump = json.dumps(self.response)
            self.match.getWhite().write_message (self.dump)

            self.response = {}
            self.response['status'] = 'success'
            self.response['type'] = 'preflop'
            self.data = {}
            self.data['preflop'] = self.match.getPreflop (4, 2)
            self.response['data'] = self.data
            self.dump = json.dumps(self.response)
            self.match.getBlack().write_message(self.dump)










