#! /usr/bin/env python

from SocketServer import (ThreadingTCPServer as TCP, StreamRequestHandler as SRH)
from time import ctime

HOST = ''
PORT = 21568
BUFSIZE = 1024
ADDR = (HOST, PORT)

CLIENT_ADDR = []

class MyRequestHandle(SRH):
    def handle(self):
        print '...connected from:', self.client_address

        if self.wfile not in CLIENT_ADDR:
            CLIENT_ADDR.append(self.wfile)
        while True:
            msg = self.rfile.readline()
            if not msg:
                break
            self.broadcast(msg)

    def broadcast(self,msg):
        print len(CLIENT_ADDR)
        for addr in CLIENT_ADDR:
            addr.write("[%s]: %s" % (self.client_address, msg))


tcpServ = TCP(ADDR, MyRequestHandle)
print 'waiting for connection...'
tcpServ.serve_forever()