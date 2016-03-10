#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import struct
import sys
import time

SERVER = '192.168.1.2'  # TODO: Adjust to the IP-address of your Arduino board!

#SERVER = 'localhost'
#SERVER = socket.gethostname()
PORT = 6734

CONNECT_REQ = (
    0x27,   ##  Start Delimiter
    0x0e,   ##  Length
    0xfe,   ##  Destination Address
    0x01,   ##  Source Address
            ##
    0x00,   ##  Class 0: Protocol Data
    0x02,   ##  OS=0 (GET), Length=2
    0x02,   ##  df_buf_len
    0x03,   ##  unit_bus_mode
    0x04,   ##  Class 4: Configuration Data
    0x02,   ##  OS=0 (GET), Length=2
    0x2e,   ##  unit_addr
    0x2f,   ##  group_addr
    0x02,   ##  Class 2: Measured Data
    0x02,   ##  OS=0 (GET), Length=2
    0x94,   ##  unit_family
    0x95,   ##  unit_type
            ##
    0xa2,   ##  CRC high
    0xaa    ##  CRC low
)

socket.setdefaulttimeout(0.5)

def hexDump(data):
    return [hex(x) for x in data]

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(0.5)

    conn = s.connect((SERVER, PORT))
except Exception as e:
    print(e.message)
    msg = "%s: %s -- Press Return to exit." % (e.errno, e.message)
    raw_input(msg)
    sys.exit(1)
print("TCP-client up and running.")

while True:
    print("Connect request...")
    try:
        s.send(bytearray(CONNECT_REQ))
    except socket.error as e:
         #print(str(e))
         if e.errno != 32: # 'Broken pipe' error isn't that dramatic.
              raise
    try:
      data = s.recv(1024)
      print("Response: ", hexDump(bytearray(data)))
    except Exception as e:
        print("Response: ", str(e))
    time.sleep(1.0)
s.close()

