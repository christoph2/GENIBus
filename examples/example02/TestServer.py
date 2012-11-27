#!/usr/bin/env python
# -*- coding: utf-8 -*-
## 
import asyncore
import socket
import sys
##import pdb
PORT = 6734
##pdb.set_trace()

##ADDR = (socket.gethostname(), PORT)
ADDR = (socket.gethostbyname(socket.gethostname()), PORT)  ##display the numeric IP address

class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(1024)
        if data:
            #print data
            with file('genibus.log', 'a') as outf:
                outf.write("%s\n" % data)


class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(ADDR)
        self.listen(5)
        print "TCP-Server [%s:%u] up and running." % ADDR

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            print '...connected from: %s' % repr(addr)
            handler = EchoHandler(sock)

    def handle_close(self):
        print "handle close"
        self.close()

##
##    def handle_error(self):
##        print "handle error"
##

    def handle_expt(self):
        print "handle expt"

    def handle_expt_event(self):
        print "handle expt event"

server = EchoServer(socket.gethostname(), PORT)
asyncore.loop()


