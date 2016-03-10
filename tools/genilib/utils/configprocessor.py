#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2014 by Christoph Schueler <github.com/Christoph2,
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

from collections import defaultdict, namedtuple, OrderedDict
import logging
import unittest
import re

SECTION = re.compile(r'^\[(?P<name>[^]]*)\]$')
PROPERTY = re.compile(r'^(?P<property>[^=]*)=\s*(?P<value>.*)$')

##
## Similiar to Python's 'ConfigParser' module, but less annoying...
##

class ConfigProcessor(object):
    """Basic ini. file reader/writer.
    """

    def __init__(self, defaults = (), logger = None):
        self._sections = OrderedDict()
        for section, items in defaults:
            self._sections[section] = OrderedDict(items)
        self._logger = logger or logging.getLogger()

    def read(self, fp):
        currentSection = None
        for line in fp.read().splitlines():
            line = line.split('#', 2)
            line = line[0]
            line = line.strip()
            if not line: continue
            match = SECTION.match(line)
            if match:
                currentSection = match.group('name')
            else:
                match = PROPERTY.match(line)
                if match:
                    prop = match.group('property')
                    prop = prop.strip().strip()
                    value = match.group('value').strip()
                    if not currentSection in self._sections:
                        self._sections[currentSection] = OrderedDict()

                    type_ = self._getType(currentSection, prop)
                    if type_ is None:
                        type_ = str

                    self._sections[currentSection][prop] = type_(value)

                else:
                    self._logger.error("Malformed Configuration Entry '%s' Check file: '%s'" % (line, fp.name))

    def write(self, fp):
        for section, items in self._sections.items():
            fp.write("[%s]\n" % section)
            for key, value in items.items():
                fp.write("%s = %s\n" % (key, value))
            fp.write("\n")

    def get(self, section, option):
        item = self._sections.get(section)
        return item.get(option) if item else None

    def items(self, section):
        items = self._sections.get(section)
        return items.items() if items else []

    def options(self, section):
        items = self._sections.get(section)
        return items.keys() if items else []

    def set(self, section, option, value):
        type_ = self._getType(section, option)
        self._sections[section][option] = type_(value)

    def add(self, section, option, value):
        #print("Adding", section, option)
        if not section in self._sections.keys():
            #print("Section '%s' does not exist!" % section)
            self._sections[section] = OrderedDict()
        if not option in self._sections[section].keys():
            #print("Option '%s' does not exist!" % option)
            pass
        #print("Value", value)
        type_ = type(value)
        self._sections[section][option] = type_(value)

    def has_option(self, section, option):
        if not section in self._sections:
            return False
        else:
            return self._sections.get(section).has_key(option)

    def has_section(self, section):
        return section in self._sections

    def _getType(self, section, option):
        if self._sections[section].has_key(option):
            return type(self._sections[section][option])
        else:
            return

    def __str__(self):
        return str(self._sections)

    __repr__ = __str__

    def _getSections(self):
        return self._sections.keys()

    sections = property(_getSections)

