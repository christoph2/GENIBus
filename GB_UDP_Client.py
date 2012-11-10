#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys

SERVER = '192.168.100.20'  # TODO: Adjust to the IP-address of your Arduino board!
PORT = 6734

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER, PORT))
except Exception as e:
    msg = "%u: %s -- Press any key to exit." % (e.errno, e.strerror)
    raw_input(msg)
    sys.exit(1)
print "UDP-client up and running."

while True:
    data = s.recv(1024)
    print repr(data)
s.close()
