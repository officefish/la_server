__author__ = 'inozemcev'
from threading import Timer
import time

class RenewableTimer():

    def __init__(self, timeout, callback):
        self.timeout = timeout
        self.callback = callback
        self.timer = Timer(timeout, callback)
        self.cancelFlag = False;

    def cancel(self):
        self.cancelFlag = True
        self.timer.cancel()

    def start(self):
        self.start_time = time.time()
        self.timer.start()

    def pause(self):
        self.cancel_time = time.time()
        self.timer.cancel()
        return self.get_actual_time()

    def resume(self):
        if self.cancelFlag:
            return self.timeout

        self.timeout = self.get_actual_time()
        self.timer = Timer(self.timeout, self.callback)
        self.start_time = time.time()
        self.timer.start()
        return self.timeout

    def get_actual_time (self):
        return self.timeout - (self.cancel_time - self.start_time)





