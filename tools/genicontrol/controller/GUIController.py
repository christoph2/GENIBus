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

import wx
from genicontrol.model.config import DataitemConfiguration
from genicontrol.controller.ControllerIF import IController
from wx.lib.pubsub import Publisher as Publisher

class GUIController(IController):

    def __init__(self, modelCls, view):
        Publisher().subscribe(self.onChange, 'Measurements')
        Publisher().subscribe(self.onChange, 'References')
        Publisher().subscribe(self.onQuit, 'QUIT')

        super(GUIController, self).__init__(modelCls, view)

        self._view = view
        self._view.Bind(wx.EVT_CLOSE, self.onCloseApplication)



    def onChange(self, msg):
        if len(msg.topic) == 1:
            group = msg.topic[0]
            item = ''
        else:
            group, item = msg.topic
        print "GROUP: '%s' ITEM: '%s' DATA: '%s'" % (group, item, msg.data)

    def onQuit(self, msg):
        self.quitApplication()

    def onCloseApplication(self, event):
        self.quitApplication()

    def quitApplication(self):
        self._view.shutdownView()
        self._model.quit()

