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

from collections import namedtuple
import wx
import genicontrol.controlids as controlids
from genicontrol.model.config import DataitemConfiguration
import genicontrol.dataitems as dataitems
from genicontrol.view.statuspanel import StatusPanel

ToggleButton = namedtuple('ToggleButton', 'id, labelOn, labelOff attrName')

def createToggleButton(parent, buttonDesc, sizer):
    btn = wx.ToggleButton(parent, label = buttonDesc.labelOn, id = buttonDesc.id)
    sizer.Add(btn, 1, wx.ALL, 5)
    setattr(parent, buttonDesc.attrName, btn)
    return btn

class Controls(wx.Panel):
    def __init__(self, parent):
        self.toggleButtons = (
            ToggleButton(controlids.ID_CMD_REMOTE_LOCAL, 'Remote', 'Local', 'btnRemoteLocal'),
            ToggleButton(controlids.ID_CMD_START_STOP, 'Start', 'Stop', 'btnStartStop'),
        )
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)
        sizer1 = wx.BoxSizer(wx.VERTICAL)

        sizer3 = wx.BoxSizer(wx.HORIZONTAL)

        sizer3.Add(wx.StaticText(self, -1, ''), 1, wx.ALL, 5)
        self.btnRefUp = wx.Button(self, label = '+', id = controlids.ID_CMD_REF_UP)
        sizer3.Add(self.btnRefUp, 1, wx.ALL | wx.GROW, 5)
        self.btnRefDown = wx.Button(self, label = '-', id = controlids.ID_CMD_REF_DOWN)
        sizer3.Add(self.btnRefDown, 1, wx.ALL | wx.GROW, 5)
        sizer1.Add(sizer3)#, 1, wx.ALL, 5)

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        for btn in self.toggleButtons:
            createToggleButton(self, btn, sizer2)

        btn = wx.Button(self, label = 'Min', id = controlids.ID_CMD_MIN)
        sizer2.Add(btn, 1, wx.ALL, 5)
        btn = wx.Button(self, label = 'Max', id = controlids.ID_CMD_MAX)
        sizer2.Add(btn, 1, wx.ALL, 5)

        sizer1.Add(sizer2) # , 1, wx.ALL, 5)
        self.SetSizer(sizer1)

        self.enableControls((controlids.ID_CMD_MAX, controlids.ID_CMD_MIN))

    def toggledbutton(self, event):
        # Active State
        if self.btn.GetValue() == True:
            self.btn.SetLabel('Stop')
            self.btn.SetBackgroundColour(wx.Color(0, 255, 0))
        # Inactive State
        if self.btn.GetValue() == False:
            self.btn.SetLabel('Start')
            self.btn.SetBackgroundColour(wx.Color(255, 0, 0))

    def setRemoteMode(self):
        pass

    def setLocalMode(self):
        pass

    def setStartMode(self):
        pass

    def setStopMode(self):
        pass

    def enableControls(self, controlIDs):
        for controlID in controlIDs:
            control = self.FindWindowById(controlID)
            control.Enable(True)

    def disableControls(self, controlIDs):
        for controlID in controlIDs:
            control = self.FindWindowById(controlID)
            control.Enable(False)

class MCPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)

        sizer = wx.BoxSizer(wx.VERTICAL)

        statusPanel = StatusPanel(self)
        sizer.Add(statusPanel) # , wx.GROW | wx.ALL, 5)
        controlsPanel = Controls(self)
        sizer.Add(controlsPanel) #, 1, wx.ALL | wx.GROW, 5)

        self.SetSizer(sizer)
        sizer.Layout()
        sizer.Fit(self)
