__author__ = 'inozemcev'
import signal
import time

import tornado.httpserver
import tornado.ioloop as loop

from django.core.management.base import BaseCommand, CommandError

#from privatemessages.tornadoapp import application

import logging
logger = logging.getLogger('tornado_commander')

from game.tornado.lobby import MainHandler, LobbyHandler, GrahhHandler, GrahhApiHandler
from game.tornado.match import MatchHandler

class Command(BaseCommand):

    args = '[port_number]'
    help = 'Starts the Tornado application for message handling.'

    def sig_handler(self, sig, frame):
        """Catch signal and init callback"""
        tornado.ioloop.IOLoop.instance().add_callback(self.shutdown)

    def shutdown(self):
        """Stop server and add callback to stop i/o loop"""
        self.http_server.stop()

        msg = 'Tornado Launcher. IOLoop.instance stop'
        logger.debug(msg)

        io_loop = tornado.ioloop.IOLoop.instance()
        io_loop.add_timeout(time.time() + 2, io_loop.stop)

    def handle(self, *args, **options):

        urls = [
            (r'/(?P<apikey>.+)/', MainHandler),
            (r'/lobby', LobbyHandler),
            (r'/match/([0-9]+)', MatchHandler),
            (r'/crossdomain.xml', GrahhHandler),
             (r'/api/crossdomain.xml', GrahhApiHandler)
        ]

        app = tornado.web.Application(urls)

        port = 8003
        address =  "5.101.123.195"

        self.http_server = tornado.httpserver.HTTPServer(app)
        self.http_server.listen(port, address=address)


        #pool = tornadoredis.ConnectionPool(host=address, port=8003)
        #c = tornadoredis.Client(connection_pool=pool)
        #c.connect()
        #c.psubscribe("*", lambda msg: c.listen(ThreadHandler.pubsub_message))


        # Init signals handler
        signal.signal(signal.SIGTERM, self.sig_handler)

        # This will also catch KeyboardInterrupt exception
        signal.signal(signal.SIGINT, self.sig_handler)


        msg = 'Tornado Launcher. IOLoop.instance start'
        logger.debug(msg)
        loop.IOLoop.instance().start()





