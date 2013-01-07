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
import threading


class Config(object):
    _lock = threading.Lock()
    logger = logging.getLogger("genicontrol")

    def __new__(cls):
        try:
            cls._lock.acquire()
            if not hasattr(cls, '_instance'):
                cls._instance = super(cls.__class__, cls).__new__(cls)
        finally:
            cls._lock.release()
        return cls._instance

        """
        config = configparser.ConfigParser()
        config.add_section('window')
        x, y = self.GetSize()
        config.set('window', 'sizeX', x)
        config.set('window', 'sizeY', y)
        x, y = self.GetPosition()
        config.set('window', 'posX', x)
        config.set('window', 'posY', y)
        fout = file('GeniControl.cfg', 'w')
        # os.path.abspath(os.path.expanduser('~/.GeniControl.cfg'))
        config.write(fout)
        fout.close()
        """

def main():
    pass

if __name__ == '__main__':
    main()


