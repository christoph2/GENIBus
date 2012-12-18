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

import wx
import genicontrol.dataitems as dataitems
#import genicontrol.view
#from genicontrol.view.mcpanel import MCPanel
#from genicontrol.view.refpanel import RefPanel
#import genicontrol.model.NullModel as NullModel
from genicontrol.model.config import DataitemConfiguration
import genicontrol.controlids as controlids

class RefPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)

        sizer = self.addValues()
        self.btnSetRefValues = wx.Button(self, label = "Set Reference Values", id = controlids.ID_SET_REFERENCE_VALUES)

        static_box = wx.StaticBox(self, label = 'Control-Mode')
        groupSizer = wx.StaticBoxSizer(static_box, wx.HORIZONTAL)
        btnConstPressure = wx.ToggleButton(self, label = 'Constant Pressure', id = controlids.ID_CMD_CONST_PRESS)
        groupSizer.Add(btnConstPressure, 1, wx.ALL, 5)
        btnPropPressure = wx.ToggleButton(self, label = 'Proportional Pressure', id = controlids.ID_CMD_PROP_PRESS)
        groupSizer.Add(btnPropPressure, 1, wx.ALL, 5)
        btnConstFreq = wx.ToggleButton(self, label = 'Constant Frequency', id = controlids.ID_CMD_CONST_FREQ)
        groupSizer.Add(btnConstFreq, 1, wx.ALL, 5)
        btnAutomatic = wx.ToggleButton(self, label = 'Automatic', id = controlids.ID_CMD_AUTOMATIC)
        groupSizer.Add(btnAutomatic, 1, wx.ALL, 5)

        #sl = wx.StaticLine(self)
        #groupSizer.Add(sl)
        sizer.Add(groupSizer, (len(DataitemConfiguration['ReferenceValues']), 0), (1, 3), wx.ALL | wx.GROW, 5)

        sizer.Add(self.btnSetRefValues, ((len(DataitemConfiguration['ReferenceValues']) + 1), 0), wx.DefaultSpan, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.SetSizer(sizer)

    def addValues(self):
        sizer = wx.GridBagSizer(5, 45)
        for idx, item in enumerate(DataitemConfiguration['ReferenceValues']):
            key, displayName, unit = item
            ditem =  dataitems.REFERENCES[key]

            ctrl = wx.StaticText(self, wx.ID_ANY, displayName, style = wx.ALIGN_RIGHT)
            ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 0), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.TextCtrl(self, wx.ID_ANY, "n/a", style = wx.ALIGN_RIGHT)
            ctrl.Enable(False)
            ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 1), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.StaticText(self, wx.ID_ANY, unit, style = wx.ALIGN_LEFT)
            sizer.Add(ctrl, (idx, 2), wx.DefaultSpan, wx.ALL | wx.ALIGN_RIGHT, 5)
        return sizer


    def setControlMode(self, mode, unset = False):
        if mode == CONTROL_MODE_AUTOMATIC:
            controlID = ID_CMD_AUTOMATIC
        elif mode == CONTROL_MODE_CONSTANT_PRESSURE:
            controlID = ID_CMD_CONST_PRESS
        elif mode == CONTROL_MODE_PROPORTIONAL_PRESSURE:
            controlID = ID_CMD_PROP_PRESS
        elif mode == CONTROL_MODE_CONSTANT_FREQUENCY:
            controlID = ID_CMD_CONST_FREQ
        control = self.FindWindowById(controlID)


