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
import genicontrol.dataitems as dataitems
from genicontrol.model.config import DataitemConfiguration
import genicontrol.controlids as controlids

CONTROL_MODE_AUTOMATIC              = 0
CONTROL_MODE_CONSTANT_PRESSURE      = 1
CONTROL_MODE_PROPORTIONAL_PRESSURE  = 2
CONTROL_MODE_CONSTANT_FREQUENCY     = 3

CONTROL_MODE_MAP = {
    CONTROL_MODE_AUTOMATIC:             controlids.ID_CMD_AUTOMATIC,
    CONTROL_MODE_CONSTANT_PRESSURE:     controlids.ID_CMD_CONST_PRESS,
    CONTROL_MODE_PROPORTIONAL_PRESSURE: controlids.ID_CMD_PROP_PRESS,
    CONTROL_MODE_CONSTANT_FREQUENCY:    controlids.ID_CMD_CONST_FREQ
}

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
        self.btnBgColor = btnAutomatic.GetBackgroundColour()
        groupSizer.Add(btnAutomatic, 1, wx.ALL, 5)
        self.setControlMode(CONTROL_MODE_AUTOMATIC)

        btnConstPressure.controlMode = CONTROL_MODE_CONSTANT_PRESSURE
        btnPropPressure.controlMode = CONTROL_MODE_PROPORTIONAL_PRESSURE
        btnConstFreq.controlMode = CONTROL_MODE_CONSTANT_FREQUENCY
        btnAutomatic.controlMode = CONTROL_MODE_AUTOMATIC

        self.Bind(wx.EVT_TOGGLEBUTTON, self.choiceButton, btnConstPressure)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.choiceButton, btnPropPressure)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.choiceButton, btnConstFreq)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.choiceButton, btnAutomatic)

        sizer.Add(groupSizer, (len(DataitemConfiguration['ReferenceValues']), 0), (1, 3), wx.ALL | wx.GROW, 5)
        sizer.Add(self.btnSetRefValues, ((len(DataitemConfiguration['ReferenceValues']) + 1), 0), wx.DefaultSpan, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.SetSizerAndFit(sizer)

    def choiceButton(self, event):
        self.setControlMode(event.EventObject.controlMode)

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
            sizer.Add(ctrl, (idx, 2), wx.DefaultSpan, wx.ALL | wx.ALIGN_LEFT, 5)
        return sizer

    def getButtonForMode(self, mode):
        controlID = CONTROL_MODE_MAP[mode]
        control = self.FindWindowById(controlID)
        return control

    def setControlMode(self, mode):
        if hasattr(self, '_mode'):
            control = self.getButtonForMode(self._mode)
            control.SetValue(False)
            control.SetBackgroundColour(self.btnBgColor)
        self._mode = mode
        control = self.getButtonForMode(mode)
        control.SetValue(True)
        control.SetBackgroundColour(wx.Color(0, 255, 0))

    def getControlMode(self):
        return self._mode

"""
    def toggledbutton(self, event):
        # Active State
        if event.EventObject.GetValue() == True:
            event.EventObject.SetLabel(event.EventObject.labelOff)
            event.EventObject.SetBackgroundColour(wx.Color(0, 255, 0))
        # Inactive State
        if event.EventObject.GetValue() == False:
            event.EventObject.SetLabel(event.EventObject.labelOn)
            event.EventObject.SetBackgroundColour(event.EventObject.bgColor)
"""
