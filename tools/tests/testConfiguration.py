#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from genilib.configuration import Config as Config


class TestCase(unittest.TestCase):

    def setUp(self):
        self.config = Config("GeniControl")
        self.config.load()

    def getPollingInterval(self):
        self.assertEqual(self.config.get('general', 'pollinginterval'), 2)

    def testGetSize(self):
        size = (self.config.get('window', 'sizex'), self.config.get('window', 'sizey'))
        self.assertEqual(size, (800, 600))

    def testGetPos(self):
        pos = (self.config.get('window', 'posx'), self.config.get('window', 'posy'))
        self.assertEqual(pos, (0, 0))

    def testGetSerial(self):
        self.assertEqual(self.config.get('serial', 'serialport'), '/dev/ttyUSB0')

    def testGetServerIp(self):
        self.assertEqual(self.config.get('network', 'serverip'), '192.168.178.22')

    def testGetSubnetMask(self):
        self.assertEqual(self.config.get('network', 'subnetmask'), '255.255.255.0')

    def testGetServerPort(self):
        self.assertEqual(self.config.get('network', 'serverport'), 8080)

    def testGetNetworkDriver(self):
        self.assertEqual(self.config.get('network', 'driver'), 1)

if __name__ == '__main__':
    unittest.main()

