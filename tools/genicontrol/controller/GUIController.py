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

import logging
import threading
import wx
import yaml
from genicontrol.model.config import DataitemConfiguration
import genicontrol.defs as defs
from genicontrol.scaling import getScalingInfo
from genicontrol.controller.ControllerIF import IController
import genicontrol.dd as dd
#from wx.lib.pubsub import Publisher as Publisher
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub as Publisher
from wx import CallAfter


class InfoWriter(object):
    def __init__(self, fname):
        self._file = file(fname, 'w')

    def __del__(self):
        self._file.close()

    def write(self, data):
        self._file.write(data)


class ControllerThread(threading.Thread):
    logger = logging.getLogger("GeniControl")

    def __init__(self, model, view, quitEvent):
        super(ControllerThread, self).__init__()
        self._model = model
        self._view = view
        self.quitEvent = quitEvent
        self.infoRecords = []
        self.setName(self.__class__.__name__)
        Publisher.subscribe(self.onInfoUpdate, 'INFO')
        Publisher.subscribe(self.onPumpStatus, 'PUMP_STATUS')
        for klass in defs.ADPUClass.nameDict.values():
            Publisher.subscribe(self.onChange, klass)

        controls = self._view.notebook.mcPanel.controlsPanel
        controls.btnOperationMode.Bind(controls.btnOperationMode.EVT_BUTTON_CHANGED, self.onOperationModeChanged)
        controls.btnRemoteLocal.Bind(controls.btnRemoteLocal.EVT_BUTTON_CHANGED, self.onRemoteLocalChanged)
        controls.btnRefUp.Bind(wx.EVT_BUTTON, self.onRefUp)
        controls.btnRefDown.Bind(wx.EVT_BUTTON, self.onRefDown)

        controls = self._view.notebook.mcPanel.alarmPanel
        controls.btnResetAlarm.Bind(wx.EVT_BUTTON, self.onResetAlarm)
        controls.btnResetAlarmLog.Bind(wx.EVT_BUTTON, self.onResetAlarmLog)

    def run(self):
        name = self.getName()
        print("Starting %s." % name)
        while True:
            if self.quitEvent.wait(0.5):
                break

        try:
            unitFamily = self._model.getValue(defs.ADPUClass.MEASURERED_DATA, 'unit_family')
            unitType = self._model.getValue(defs.ADPUClass.MEASURERED_DATA, 'unit_type')
        except KeyError:
            self.logger.debug("unitFamily and unitType not available.")
        #unitVersion = self._model.getValue(defs.ADPUClass.MEASURERED_DATA, 'unit_version') ## TODO: Fixme!
        else:
            with file(dd.getDeviceFilePath(unitFamily, unitType, 1), 'w') as outf:
                #outf.write(str(self.infoRecords))
                yaml.dump(self.infoRecords, outf)

        print("Exiting %s." % name)

    def onInfoUpdate(self, msg):
        #self._view.post('INFO_UPDATE', msg)
        for values in msg.data.values():
            for key, value in values.items():
                svalue = getScalingInfo(value)
                CallAfter(self._view.notebook.infoPanel.setItem, key, svalue.physEntity, str(svalue.factor), svalue.unit, str(value.zero), str(value.range))
                CallAfter(self._view.notebook.infoPanel.grid.Fit)
                #self._view.notebook.infoPanel.setItem(key, svalue.physEntity, str(svalue.factor), svalue.unit, str(value.zero), str(value.range))
                #self._view.notebook.infoPanel.grid.Fit()
        self.infoRecords.append(values)
        #print(msg.data.values())

    def onChange(self, msg):
        if len(msg.topic) == 1:
            group = msg.topic[0]
            item = ''
        else:
            group, item = msg.topic
        #print("Update: '%s' Item:'%s' Data: '%s'" % (group, item, msg.data))
        if group == 'MEASURERED_DATA':
            CallAfter(self._view.notebook.mcPanel.setValue, item, msg.data)
            #self._view.notebook.mcPanel.setValue(item, msg.data)

    def onPumpStatus(self, msg):
        group, item = msg.topic
        data = msg.data
        #print("***PS***", item, data)
        CallAfter(self._view.notebook.mcPanel.setPumpStatus, item, data)
        #self._view.notebook.mcPanel.setPumpStatus(item, data)

    def onRemoteLocalChanged(self, event):
        print("Remote?: %s\n" % (event.getState(), ))
        cmd = 'REMOTE' if event.getState() else 'LOCAL'
        self.sendCommand(cmd)

    def onOperationModeChanged(self, event):
        print("Operation-Mode changed: '%s'" % event.getState())
        self.sendCommand(event.getState().upper())

    def onRefUp(self, event):
        print("RefUp")
        self.sendCommand('REF_UP')

    def onRefDown(self, event):
        print("RefDown")
        self.sendCommand('REF_DOWN')

    def onResetAlarm(self, event):
        print("ResetAlarm")
        self.sendCommand('RESET_ALARM')

    def onResetAlarmLog(self, event):
        print("ResetAlarmLog")
        self.sendCommand('RESET_ALARM_LOG')

    def sendCommand(self, command):
        self._model.sendCommand(command)


class GUIController(IController):
    def __init__(self, modelCls, view):
        self._view = view
        self._view.Bind(wx.EVT_CLOSE, self.onCloseApplication)
        Publisher.subscribe(self.onQuit, 'QUIT')

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
        self._model.quit()
        self._view.shutdownView()

