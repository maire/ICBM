__author__ = 'herschel'

import SocketServer

class ICBMReceiver:

    def __init__(self, log_queue):

        host, port = 'localhost', 9999
        self.server = SocketServer.UDPServer((host, port), self.ICBMHandler)
        self.server.log_queue = log_queue

    def run(self):

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.server.shutdown()

    class ICBMHandler(SocketServer.BaseRequestHandler):

        def handle(self):

            data = self.request[0]
            socket = self.request[1]
            self.server.log_queue.put((data, self.client_address[0]))
