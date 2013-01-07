#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2012 by Christoph Schueler <github.com/Christoph2,
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


import locale
import logging
from gettext import ugettext as _TR
#_ = gettext.translation(my_program_name).ugettext
import gettext


logger = logging.getLogger("genicontrol")

##t = gettext.translation('spam', '/usr/share/locale')
##_ = t.ugettext
##gettext.install('myapplication', '/usr/share/locale', unicode=1)


def initialize(appName):
    shortLocale, codepage = locale.getdefaultlocale()


    gettext.bindtextdomain(appName, './locale')
    gettext.textdomain(appName)
    gettext.install(appName, './locale', unicode = True)

    #self.presLan_en = gettext.translation(appName, "./locale", languages = ['en'])
    #self.presLan_de = gettext.translation(appName, "./locale", languages = ['de'])
    #self.presLan_it = gettext.translation(appName, "./locale", languages = ['it'])
    #self.presLan_en.install()

    try:
        canonicalLocale = locale.setlocale(locale.LC_ALL, (locale.normalize(shortLocale), 'UTF8'))
    except locale.Error:
        canonicalLocale = locale.setlocale(locale.LC_ALL, '')
    glob= globals()
    glob['shortLocale'] = shortLocale
    glob['codepage'] = codepage
    glob['canonicalLocale'] = canonicalLocale


