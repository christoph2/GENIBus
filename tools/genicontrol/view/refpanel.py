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
#import math
#import genicontrol.conversion as conversion

import wx
import math
import threading
import genicontrol.apdu as apdu
import genicontrol.defs as defs
#import genicontrol.model.ModelIf as ModelIf
from wx.lib.scrolledpanel import ScrolledPanel
import genicontrol.dataitems as dataitems
from genicontrol.model.config import DataitemConfiguration, REFERENCES_DICT
import genicontrol.controlids as controlids
from decimal import Decimal as D
from genilib.utils import dumpHex, makeWord

CONTROL_MODE_AUTOADAPT              = 0
CONTROL_MODE_CONSTANT_PRESSURE      = 1
CONTROL_MODE_PROPORTIONAL_PRESSURE  = 2
CONTROL_MODE_CONSTANT_FREQUENCY     = 3

CONTROL_MODE_MAP = {
    CONTROL_MODE_AUTOADAPT:             controlids.ID_CMD_AUTOADAPT,
    CONTROL_MODE_CONSTANT_PRESSURE:     controlids.ID_CMD_CONST_PRESS,
    CONTROL_MODE_PROPORTIONAL_PRESSURE: controlids.ID_CMD_PROP_PRESS,
    CONTROL_MODE_CONSTANT_FREQUENCY:    controlids.ID_CMD_CONST_FREQ
}

class RefPanel(ScrolledPanel):
    def __init__(self, parent):
        self._concurrentAccess = threading.Lock()
        self._refsetRequested = False
        self._connected = False
        #self._model = model

        ScrolledPanel.__init__(self, parent = parent, id = wx.ID_ANY)

        sizer = self.addValues()

        self.btnSetRefValues = wx.Button(self, label = "Set Reference Value", id = controlids.ID_SET_REFERENCE_VALUES)
        sizer.Add(self.btnSetRefValues, (len(DataitemConfiguration['ReferenceValues']), 0), wx.DefaultSpan, wx.ALL | wx.ALIGN_LEFT, 5)
        self.btnSetRefValues.Bind(wx.EVT_BUTTON, self.onRefSet)

        height = ['1.5', '2.0', '2.5', '3.0', '3.5']
        self.cb = wx.ComboBox(self, choices=height, style=wx.CB_READONLY)
        self.cb.SetSelection(2)
        sizer.Add(self.cb, (len(DataitemConfiguration['ReferenceValues']), 1), wx.DefaultSpan, wx.ALL | wx.ALIGN_RIGHT, 5)
        self.cb.Bind(wx.EVT_COMBOBOX, self.onSelect)
        ctrl = wx.StaticText(self, wx.ID_ANY, "m", style = wx.ALIGN_RIGHT)
        sizer.Add(ctrl, (len(DataitemConfiguration['ReferenceValues']), 2), wx.DefaultSpan, wx.ALL | wx.ALIGN_LEFT, 5)

        static_box = wx.StaticBox(self, label = 'Control-Mode')
        groupSizer = wx.StaticBoxSizer(static_box, wx.HORIZONTAL)
        btnConstPressure = wx.ToggleButton(self, label = 'Constant Pressure', id = controlids.ID_CMD_CONST_PRESS)
        groupSizer.Add(btnConstPressure, 1, wx.ALL, 5)
        btnPropPressure = wx.ToggleButton(self, label = 'Proportional Pressure', id = controlids.ID_CMD_PROP_PRESS)
        groupSizer.Add(btnPropPressure, 1, wx.ALL, 5)
        btnConstFreq = wx.ToggleButton(self, label = 'Constant Frequency', id = controlids.ID_CMD_CONST_FREQ)
        groupSizer.Add(btnConstFreq, 1, wx.ALL, 5)
        btnAutoAdapt = wx.ToggleButton(self, label = 'AutoAdapt', id = controlids.ID_CMD_AUTOADAPT)
        self.btnBgColor = btnAutoAdapt.GetBackgroundColour()
        groupSizer.Add(btnAutoAdapt, 1, wx.ALL, 5)
        self.setControlMode(CONTROL_MODE_CONSTANT_PRESSURE)

        btnConstPressure.controlMode = CONTROL_MODE_CONSTANT_PRESSURE
        btnPropPressure.controlMode = CONTROL_MODE_PROPORTIONAL_PRESSURE
        btnConstFreq.controlMode = CONTROL_MODE_CONSTANT_FREQUENCY
        btnAutoAdapt.controlMode = CONTROL_MODE_AUTOADAPT

        self.Bind(wx.EVT_TOGGLEBUTTON, self.choiceButton, btnConstPressure)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.choiceButton, btnPropPressure)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.choiceButton, btnConstFreq)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.choiceButton, btnAutoAdapt)

        sizer.Add(groupSizer, ((len(DataitemConfiguration['ReferenceValues']) + 1), 0), (1, 3), wx.ALL | wx.GROW, 5)

        self.SetSizerAndFit(sizer)
        self.SetupScrolling()

        self.itemDict = dict([(x[0], x[1:]) for x in DataitemConfiguration['ReferenceValues']])

    def choiceButton(self, event):
        self.setControlMode(event.EventObject.controlMode)

    def addValues(self):

        sizer = wx.GridBagSizer(hgap=5, vgap=5)

        for idx, item in enumerate(DataitemConfiguration['ReferenceValues']):
            key, displayName, unit, controlIdValue, controlIdUnit = item

            if key in ('ref_rem', 'ref_ir'):
                ditem = dataitems.REFERENCES[key]
            else:
                ditem = dataitems.MEASUREMENT_VALUES[key]

            ctrl = wx.StaticText(self, wx.ID_ANY, displayName, style = wx.ALIGN_RIGHT)
            ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 0), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.TextCtrl(self, controlIdValue, "n/a", style = wx.ALIGN_RIGHT)
            ctrl.Enable(False)
            ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 1), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.StaticText(self, controlIdUnit, unit, style = wx.ALIGN_LEFT)
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
        control.SetBackgroundColour(wx.Colour(0, 255, 0))

    def getControlMode(self):
        return self._mode

    def setValue(self, item, value):
        entry = REFERENCES_DICT.get(item, None)
        if entry:
            _, _, controlID, _ = entry
            if controlID:
                control = self.FindWindowById(controlID)
                if control:
                    control.SetValue(str(value))

    def onSelect(self, event):
        cb_item = event.GetSelection()
        height = self.cb.GetValue()
        #print("cb_item:", cb_item, height)

    def writeToServer(self, req):
        self._model.writeToServer(req)
        #self._connection.write(req)
        #self._controller.trace(False, req)

    def calculateSetpoint(self, x, sys_fb_min, sys_fb_max, r_min, r_max):
#ref_rem = ((height-sys_fb_min)/(sys_fb_max - sys_fb_min)*254 - r_min)*254/(r_max-r_min)
        return ((D(x) - D(sys_fb_min)) / (D(sys_fb_max) - D(sys_fb_min)) * D('254.0') - D(r_min)) * D('254.0') / (D(r_max) - D(r_min))

    def setRefValue(self):
        x = self.cb.GetValue()
        #print("setRefValue height:", x)
        for idx, item in enumerate(DataitemConfiguration['ReferenceValues'], 1):
            key, displayName, unit, controlIdValue, controlIdUnit = item
            _, _, controlID, _ =  self.itemDict[key]
            control = self.FindWindowById(controlID)
            if key == 'r_min': r_min = control.GetValue()
            if key == 'r_max': r_max = control.GetValue()
            sys_fb_min = u'0'
            sys_fb_max = u'20'
        return self.calculateSetpoint(x, sys_fb_min, sys_fb_max, r_min, r_max)

    def onRefSet(self, event):
        self._concurrentAccess.acquire()
        self._refsetRequested = True
        req = apdu.createSetValuesPDU(
            apdu.Header(defs.SD_DATA_REQUEST, 0x20, 0x01),
            references = [('ref_rem', int(self.setRefValue()))]
        )
        #print("onRefSet:", int(self.setRefValue()), dumpHex(req))
        self.writeToServer(req)
        self._concurrentAccess.release()

#    uint8 ref_rem_set[13] = {0x27,0x09,0x20,0x01,0x03,0x81,0x07,0x05,0x82,0x01,0x53,0x00,0x00};
#    uint8 ref_ir_set[13]  = {0x27,0x06,0x20,0x01,0x05,0x82,0x02,0x53,0x00,0x00}; //2,5m
#    uint8 ref_ir_set[13]  = {0x27,0x06,0x20,0x01,0x05,0x82,0x02,0x70,0x00,0x00}; //3,0m

"""
    def toggledbutton(self, event):
        # Active State
        if event.EventObject.GetValue() == True:
            event.EventObject.SetLabel(event.EventObject.labelOff)
            event.EventObject.SetBackgroundColour(wx.Colour(0, 255, 0))
        # Inactive State
        if event.EventObject.GetValue() == False:
            event.EventObject.SetLabel(event.EventObject.labelOn)
            event.EventObject.SetBackgroundColour(event.EventObject.bgColor)
"""
