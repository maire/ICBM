__author__ = 'herschel'

import Queue
import ConfigParser
import os
import socket
from threading import Thread
from ICBM import Receiver
from ICBM.ICBM_pb2 import Log

class ICBMServer:

    BIND_ADDR = 'localhost'
    BIND_PORT = '9998'
    LOG_DIR = os.path.join(os.path.dirname(__file__))

    open_files = {}

    #log_format = '[{0: <20}][{1: <10}][{2: >8}]: {3} ({4}, {5}, {6}, {7})\n'
    log_format = '[{0: <20}][{1: <10}][{2: >8}]: {3}'

    def __init__(self):

        settings = ConfigParser.ConfigParser()
        settings.read(os.path.join(os.path.dirname(__file__), 'settings.conf'))

        for key, value in settings.items('ICBM'):
            if hasattr(self, key.upper()):
                if type(getattr(self, key.upper())) is bool:
                    setattr(self, key.upper(), True if value.lower() == 'true' else False)
                elif type(getattr(self, key.upper())) is str:
                    setattr(self, key.upper(), str(value))
                elif type(getattr(self, key.upper())) is int:
                    setattr(self, key.upper(), int(value))
                elif type(getattr(self, key.upper())) is list:
                    setattr(self, key.upper(), value.split(','))
                else:
                    raise Exception('Bad type in config file.')

        log_queue = Queue.Queue()
        log_thread = Thread(target=self.QueueProcessor, args=[log_queue])
        log_thread.daemon = True
        log_thread.start()
        server = Receiver(log_queue)
        server.run()

    def QueueProcessor(self, log_queue):
        while True:
            try:
                data = log_queue.get()
                log = Log()
                log.ParseFromString(data[0])
                hostname = socket.gethostbyaddr(data[1])[0]
                if hostname not in self.open_files:
                    self.open_files[hostname] = open(hostname + '.log', 'a')
                self.open_files[hostname].write(
                    self.log_format.format(log.time, log.server, Log.Level.Name(log.level), log.message))
                self.open_files[hostname].flush()
            except KeyboardInterrupt:
                for key, value in self.open_files:
                    value.close()

ICBMServer()
