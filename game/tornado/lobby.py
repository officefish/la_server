__author__ = 'inozemcev'

import tornado.web as web
import tornado.websocket as websocket
import json;
import redis
from random import randrange


import logging
logger =  logging.getLogger('game_handler')


class MainHandler (web.RequestHandler):


     def get(self, **params):
        self.set_header('Content-Type', 'text/plain')
        self.write('Hello, this is your params:' + str(params))


     def prepare(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "X-Thunder-Secret-Key")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, DELETE")

     def options(self, *args, **kwargs):
        pass

class LobbyHandler(websocket.WebSocketHandler):
    handlers = set ()
    players = {}

    def check_origin(self, origin):
        return True

    def open(self):
        logger.debug('SocketHandler::Open')


    def on_close(self):
        logger.debug('SocketHandler::Close')

        if LobbyHandler.handlers.__contains__(self):
            LobbyHandler.handlers.remove(self)


        response = {}
        response['status'] = 'success'
        response['type'] = 'user_leave'
        data = {}
        data['id'] = self.id
        response['data'] = data
        dump = json.dumps(response)
        LobbyHandler.send_updates(dump)




    def handle_request(self, response):
        logger.debug('Socket_handler::handle_request')
        pass

    def on_message(self, message):

        logger.debug('SocketHandler::onmessage')
        event = json.loads(message)

        type = event['type']

        if type == 'connect_to_lobby':

            self.id = event['target']
            self.hero_uid = event['hero_uid']
            self.level = event['level']
            self.deck_id = event['deck_id']
            self.hero_id = event['hero_id']

            LobbyHandler.init_player(self.id, self.level, self.deck_id, self.hero_id)

            #loadStack
            response = {}
            response['status'] = 'success'
            response['type'] = 'init_players'
            data = {}
            players = list()
            for player in LobbyHandler.handlers:
                players.append({'id':player.id, 'hero_uid':player.hero_uid, 'level':player.level})

            data['players'] = players
            response['data'] = data
            dump = json.dumps(response)
            self.write_message(dump)

            # add new unit to stack
            LobbyHandler.handlers.add(self)
            response = {}
            response['status'] = 'success'
            response['type'] = 'user_join'
            data = {}
            data['id'] = self.id
            data['hero_uid'] = self.hero_uid
            data['level'] = self.level
            response['data'] = data
            dump = json.dumps(response)
            LobbyHandler.send_updates(dump)

        elif type == 'invite_to_game':

            # send invitation
            unitId = event['data']['unit']
            unit = LobbyHandler.get_unit_by_id(unitId)

            response = {}
            response['status'] = 'success'
            response['type'] = 'invite'
            data = {}
            data['initiator'] = self.id
            data['level'] = event['data']['level']
            data['hero_uid'] = event['data']['hero_uid']
            data['mode'] = event['data']['mode']
            response['data'] = data
            dump = json.dumps(response)
            unit.write_message(dump)

            # confirm sending
            response = {}
            response['status'] = 'success'
            response['type'] = 'confirm_invite'
            data = {}
            data['level'] = event['data']['level']
            data['hero_uid'] = event['data']['hero_uid']
            data['mode'] = event['data']['mode']
            data['unit'] = unitId
            response['data'] = data
            dump = json.dumps(response)
            self.write_message(dump)

        elif type == 'cancel_invite':

            # cancel invitation
            unitId = event['data']['unit']
            unit = LobbyHandler.get_unit_by_id(unitId)

            response = {}
            response['status'] = 'success'
            response['type'] = 'cancel_invite'
            data = {}
            data['initiator'] = self.id
            response['data'] = data
            dump = json.dumps(response)
            unit.write_message(dump)

            #confirm_cancel
            response = {}
            response['status'] = 'success'
            response['type'] = 'confirm_cancel'
            data = {}
            data['unit'] = unitId
            response['data'] = data
            dump = json.dumps(response)
            self.write_message(dump)

        elif type == 'reject_invite':

            # reject invitation
            unitId = event['data']['unit']
            unit = LobbyHandler.get_unit_by_id(unitId)

            response = {}
            response['status'] = 'success'
            response['type'] = 'reject_invite'
            data = {}
            data['initiator'] = self.id
            response['data'] = data
            dump = json.dumps(response)
            unit.write_message(dump)

            #confirm_cancel
            response = {}
            response['status'] = 'success'
            response['type'] = 'confirm_reject'
            data = {}
            data['unit'] = unitId
            response['data'] = data
            dump = json.dumps(response)
            self.write_message(dump)

        elif type == 'accept_invite':

            #init game cache
            redis_client = redis.StrictRedis()

            random_int = randrange(1,500000)
            match = 'la_game_match:%d' % random_int

            player1_id = event['data']['player1']
            player2_id = event['data']['player2']

            logger.debug('player1_id:%s' % player1_id)
            logger.debug('player2_id:%s' % player2_id)

            redis_client.hset(match, 'id', random_int)
            redis_client.hset(match, 'match_type', event['data']['mode'])

            redis_client.hset(match, 'player1', player1_id)
            redis_client.hset(match, 'player2', player2_id)

            self.player1Data = LobbyHandler.get_player_data(player1_id)
            self.player2Data = LobbyHandler.get_player_data(player2_id)

            redis_client.hset(match, 'player1_deckId', self.player1Data['deckId'])
            redis_client.hset(match, 'player2_deckId', self.player2Data['deckId'])

            redis_client.hset(match, 'player1_level', self.player1Data['level'])
            redis_client.hset(match, 'player2_level', self.player2Data['level'])

            redis_client.hset(match, 'player1_heroId', self.player1Data['heroId'])
            redis_client.hset(match, 'player2_heroId', self.player2Data['heroId'])

            logger.debug(event['data']['mode'])

            response = {}
            response['status'] = 'success'
            response['type'] = 'start_match'
            data = {}
            data['match_id'] = random_int
            data['mode'] = event['data']['mode']
            response['data'] = data
            dump = json.dumps(response)


            #redirect player1 to match socket
            player1_client = LobbyHandler.get_unit_by_id(player1_id)
            player1_client.write_message (dump)

            #redirect player2 to match socket
            self.write_message(dump)

            #close player1 connection

            #close player2 connection

    @classmethod
    def get_player_data (cls, id):
        return cls.players[id]

    @classmethod
    def init_player (cls, id, level, deckId, heroId):
        cls.players[id] = {'level': level, 'deckId':deckId, 'heroId':heroId}

    @classmethod
    def get_unit_by_id (cls, id):
        for handler in cls.handlers:
            if handler.id == id:
                target = handler

        return target

    @classmethod
    def send_updates (cls, message):
        for handler in cls.handlers:
             try:
                   handler.write_message(message)
             except:
                   logging.error("Error sending message", exc_info=True)

