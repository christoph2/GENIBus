#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2013 by Christoph Schueler <github.com/Christoph2,
##                                      cpu12.gems@googlemail.com>
##
##  All Rights Reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License along
## with this program; if not, write to the Free Software Foundation, Inc.,
## 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
##
##

try:
    import ConfigParser as configparser
except ImportError:
    import configparser # Python 3.x

import logging
import os
import threading
from genicontrol.utils import absConfigurationFilename

CFG_FILE_NAME = absConfigurationFilename('.GeniControl.cfg')

class Config(object):
    _lock = threading.Lock()
    logger = logging.getLogger("genicontrol")
    loaded = False

    def __new__(cls):
        try:
            cls._lock.acquire()
            if not hasattr(cls, '_instance'):
                cls._instance = super(cls.__class__, cls).__new__(cls)
        finally:
            cls._lock.release()
        return cls._instance

    def loadConfiguration(self):
        if not self.loaded:
            self.config = configparser.ConfigParser()
            config = self.config
            config.read([CFG_FILE_NAME])
            if not config.has_section('general'):
                config.add_section('general')
                config.set('general', 'pollingInterval', '2')
            self.pollingInterval = config.getint('general', 'pollingInterval')
            if not config.has_section('network'):
                config.add_section('network')
                config.set('network', 'serverIP', '192.168.100.10')
                config.set('network', 'subnetMask', '255.255.255.0')
                config.set('network', 'serverPort', '6734')
                config.set('network', 'driver', '1')
            self.serverIP = config.get('network', 'serverIP')
            self.serverPort = config.get('network', 'serverPort')
            self.subnetMask = config.get('network', 'subnetMask')
            try:
                self.networkDriver = config.get('network', 'driver')
            except:
                self.networkDriver = '1'
            if not config.has_section('window'):
                config.add_section('window')
                config.set('window', 'sizeX', '800')
                config.set('window', 'sizeY', '600')
                config.set('window', 'posX', 0)
                config.set('window', 'posY', 0)
            self.posX = config.getint('window', 'posx')
            self.posY = config.getint('window', 'posy')
            self.sizeX = config.getint('window', 'sizex')
            self.sizeY = config.getint('window', 'sizey')
            self.loaded = True

    def saveConfiguration(self):
        print "Saving configuration..."
        config = self.config
        with open(CFG_FILE_NAME, 'w') as fout:
            config.set('window', 'sizex', str(self.sizeX))
            config.set('window', 'sizey', str(self.sizeY))
            config.set('window', 'posx', str(self.posX))
            config.set('window', 'posy', str(self.posY))
            config.set('general', 'pollingInterval', str(self.pollingInterval))
            config.set('network', 'serverIP', str(self.serverIP))
            config.set('network', 'subnetMask', str(self.subnetMask))
            config.set('network', 'serverPort', str(self.serverPort))
            config.set('network', 'driver', str(self.networkDriver))
            config.write(fout)


