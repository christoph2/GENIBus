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

import logging
import threading
import wx
from genicontrol.model.config import DataitemConfiguration
import genicontrol.defs as defs
from genicontrol.scaling import getScalingInfo
from genicontrol.controller.ControllerIF import IController
from wx.lib.pubsub import Publisher as Publisher


class ControllerThread(threading.Thread):
    logger = logging.getLogger("genicontrol")

    def __init__(self, model, view, quitEvent):
        super(ControllerThread, self).__init__()
        self._model = model
        self._view = view
        self.quitEvent = quitEvent
        self.setName(self.__class__.__name__)
        Publisher().subscribe(self.onInfoUpdate, 'INFO')
        for klass in defs.ADPUClass.nameDict.values():
            Publisher().subscribe(self.onChange, klass)


    def run(self):
        name = self.getName()
        print "Starting %s." % name
        while True:
            if self.quitEvent.wait(0.5):
                break
        print "Exiting %s." % name

    def onInfoUpdate(self, msg):
        for values in msg.data.values():
            for key, value in values.items():
                svalue = getScalingInfo(value)
                self._view.notebook.infoPanel.setItem(key, svalue.physEntity, str(svalue.factor), svalue.unit, str(value.zero), str(value.range))
                self._view.notebook.infoPanel.grid.Fit()

    def onChange(self, msg):
        if len(msg.topic) == 1:
            group = msg.topic[0]
            item = ''
        else:
            group, item = msg.topic
        #print "Update: '%s' Item:'%s' Data: '%s'" % (group, item, msg.data)


class GUIController(IController):
    def __init__(self, modelCls, view):
        self._view = view
        self._view.Bind(wx.EVT_CLOSE, self.onCloseApplication)
        Publisher().subscribe(self.onQuit, 'QUIT')

        super(GUIController, self).__init__(modelCls, view)

        self._quitEvent = threading.Event()
        self._controllerThread = ControllerThread(self._model, view, self._quitEvent)
        self._controllerThread.start()
        self.signal()

    def onQuit(self, msg):
        self.quitApplication()

    def onCloseApplication(self, event):
        self.quitApplication()

    def quitApplication(self):
        self._quitEvent.set()
        self._controllerThread.join()
        self._view.shutdownView()
        self._model.quit()

