__author__ = 'herschel'

import socket
import time
import logging
import logging.handlers
from ICBM_pb2 import Log

hostname = socket.gethostname()

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

class ICBMLauncher(logging.Handler):

    def __init__(self, host, port, level='DEBUG'):

        self.host = host
        self.port = port

        logging.Handler.__init__(self, level=level)

    def emit(self, record):

        log = Log()
        log.server = hostname
        log.time = time.strftime("%b %d %Y %H:%M:%S", time.gmtime())
        log.level = record.levelno
        log.context = record.name
        log.function = record.funcName
        log.line = record.lineno
        log.module = record.module
        log.message = record.msg
        if record.exc_info:
            log.exc_info = record.exc_info

        data = log.SerializeToString()

        sock.sendto(data, (self.host, self.port))
