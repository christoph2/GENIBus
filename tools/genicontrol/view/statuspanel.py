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
import genicontrol.controlids as controlids
import genicontrol.dataitems as dataitems
import genicontrol.leds as leds

class StatusPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)

        staticBox = wx.StaticBox(self, label = 'Pump status')
        groupSizer = wx.StaticBoxSizer(staticBox)

        sizer = self.addValues()
        ctrl = wx.StaticText(self, wx.ID_ANY, 'Performance', style = wx.ALIGN_RIGHT)
        sizer.Add(ctrl, (7, 0), wx.DefaultSpan, wx.ALL, 5)

        self.gauge = wx.Gauge(parent = self, range = 100, id = controlids.ID_MEAS_PERFORMACE)
        self.gauge.SetToolTip(wx.ToolTip('n/a'))
        self.gauge.SetValue(0)
        sizer.Add(self.gauge, (7, 1), (1, 1), wx.ALL, 5)

        ctrl = wx.StaticText(self, wx.ID_ANY, '%', style = wx.ALIGN_RIGHT)
        sizer.Add(ctrl, (7, 2), wx.DefaultSpan, wx.ALL | wx.ALIGN_RIGHT, 5)

        groupSizer.Add(sizer)
        self.SetSizerAndFit(groupSizer)
        self.itemDict = dict([(x[0], x[1:]) for x in DataitemConfiguration['MeasurementValues']])


    def addValues(self):
        sizer = wx.GridBagSizer(5, 45)

        self.ledControl = LEDPanel(self)
        sizer.Add(self.ledControl, (0, 0), wx.DefaultSpan, wx.ALL, 5)

        for idx, item in enumerate(DataitemConfiguration['MeasurementValues'], 1):
            key, displayName, unit, controlIdValue, controlIdUnit = item
            ditem =  dataitems.MEASUREMENT_VALUES[key]
            if key in ('f_act', 'unit_family', 'unit_type'):
                continue

            ctrl = wx.StaticText(self, wx.ID_ANY, displayName, style = wx.ALIGN_RIGHT)
            ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 0), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.TextCtrl(self, controlIdValue, "n/a", style = wx.ALIGN_RIGHT)
            ctrl.Enable(False)
            ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 1), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.StaticText(self, controlIdUnit, unit, style = wx.ALIGN_RIGHT)
            sizer.Add(ctrl, (idx, 2), wx.DefaultSpan, wx.ALL | wx.ALIGN_RIGHT, 5)
        return sizer

    def setValue(self, key, value):
        _, _, controlID, _ =  self.itemDict[key]
        control = self.FindWindowById(controlID)
        control.SetValue(str(value))

    def setUnit(self, key, unit):
        _, _, _, controlID =  self.itemDict[key]
        control = self.FindWindowById(controlID)
        control.SetValue(str(unit))


ALARM_LOGS =(
    (controlids.ID_ALARM_LOG1, "alarm_log_1", "Alarm Log No. 1"),
    (controlids.ID_ALARM_LOG2, "alarm_log_2", "Alarm Log No. 2"),
    (controlids.ID_ALARM_LOG3, "alarm_log_3", "Alarm Log No. 3"),
    (controlids.ID_ALARM_LOG4, "alarm_log_4", "Alarm Log No. 4"),
    (controlids.ID_ALARM_LOG5, "alarm_log_5", "Alarm Log No. 5"),
)


class AlarmPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)

        staticBox = wx.StaticBox(self, label = 'Alarm Status')
        groupSizer = wx.StaticBoxSizer(staticBox)

        sizer = wx.FlexGridSizer(rows = 8, cols = 2, hgap = 5, vgap = 5)

        st = wx.StaticText(self, wx.ID_ANY, label = "Actual Alarm")
        sizer.Add(st, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        ctrl = wx.TextCtrl(self, controlids.ID_ALARM_ACTUAL, "n/a", style = wx.ALIGN_LEFT)
        ctrl.Enable(False)
        sizer.Add(ctrl, 1, wx.ALL | wx.ALIGN_LEFT, 5)

        sizer.Add(wx.StaticText(self, label = ''), 1, wx.ALL | wx.ALIGN_LEFT, 5)
        btn = wx.Button(self, controlids.ID_CMD_RESET_ALARM, "Reset Alarm")
        sizer.Add(btn, 1, wx.ALL | wx.ALIGN_LEFT, 5)

        for controlId, name, label in ALARM_LOGS:
            ditem =  dataitems.MEASUREMENT_VALUES[name]
            st = wx.StaticText(self, wx.ID_ANY, label = label)
            sizer.Add(st, 1, wx.ALL | wx.ALIGN_LEFT, 5)

            ctrl = wx.TextCtrl(self, controlId, "n/a", style = wx.ALIGN_LEFT)
            ctrl.Enable(False)
            ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        sizer.Add(wx.StaticText(self, label = ''), 1, wx.ALL | wx.ALIGN_LEFT, 5)
        btn = wx.Button(self, controlids.ID_CMD_RESET_ALARM_LOG, "Reset Alarm Log")
        sizer.Add(btn, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        groupSizer.Add(sizer)
        self.SetSizerAndFit(groupSizer)


class LEDPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)

        self.leds = {
            'red': leds.ledRed.getBitmap(),
            'green': leds.ledGreen.getBitmap(),
            'grey': leds.ledGrey.getBitmap()
        }

        size = wx.Size(1, 0)
        for led in self.leds.values():
            size = max(size, led.GetSize())

        self.ledSize = size
        panelSize = wx.Size(((size.width * 2) + (3 * 5)), (size.height + (2 * 5)))
        self.SetMinSize(panelSize)

        self.ledRedOn = False
        self.ledGreenOn = False
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Layout()

    def setState(self, num, on):
        if num ==  0:
            self.ledGreenOn = on
            self.Refresh()
        elif num == 1:
            self.ledRedOn = on
            self.Refresh()

    def getState(self, num):
        if num == 0:
            return self.ledGreenOn
        elif num == 1:
            return self.ledRedOn

    def onPaint(self, evt):
        dc = wx.PaintDC(self)
        #dc.SetBackground(wx.Brush("WHITE"))
        dc.Clear()
        if "gtk1" in wx.PlatformInfo:
            img = bmp.ConvertToImage()
            img.ConvertAlphaToMask(220)
            bmp = img.ConvertToBitmap()
        if self.ledGreenOn:
            dc.DrawBitmap(self.leds['green'], 5, 5, True)
        else:
            dc.DrawBitmap(self.leds['grey'], 5, 5, True)
        if self.ledRedOn:
            dc.DrawBitmap(self.leds['red'], self.ledSize.width + (2 * 5), 5, True)
        else:
            dc.DrawBitmap(self.leds['grey'], self.ledSize.width + (2 * 5), 5, True)


class PumpOperationPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)
        self.items = (
            ("Operation Mode", "", controlids.ID_OPERATION_MODE),
            ("System Mode", "", controlids.ID_SYSTEM_MODE),
            ("Control Source", "", controlids.ID_CONTROL_SOURCE),

            ("Ext. Analogue", "%", controlids.ID_EXT_ANALOGUE),
            ("Total Influence", "%", controlids.ID_TOTAL_INFLUENCE),

            ("Setpoint", "m", controlids.ID_SETPOINT),
            ("Acual Setpoint", "m", controlids.ID_ACTUAL_SETPOINT),
        )
        self.itemDict = {}
        for item in self.items:
            self.itemDict[item[0]] = item
        staticBox = wx.StaticBox(self, label = 'Pump operation')
        groupSizer = wx.StaticBoxSizer(staticBox)

        sizer = self.addValues()

        groupSizer.Add(sizer)
        self.SetSizerAndFit(groupSizer)

    def getControlByName(self, name):
        _, _, ctrlId = self.itemDict[name]
        return self.FindWindowById(ctrlId)

    def setValue(self, item ,value):
        ctrl = self.getControlByName(item)
        ctrl.SetValue(value)


    def addValues(self):
        sizer = wx.GridBagSizer(5, 45)
        for idx, item in enumerate(self.items):
            displayName, unit, controlID = item

            ctrl = wx.StaticText(self, wx.ID_ANY, displayName, style = wx.ALIGN_RIGHT)
            #ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 0), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.TextCtrl(self, controlID, "n/a", style = wx.ALIGN_RIGHT)
            ctrl.Enable(False)
            #ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 1), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.StaticText(self, wx.ID_ANY, unit, style = wx.ALIGN_RIGHT)
            sizer.Add(ctrl, (idx, 2), wx.DefaultSpan, wx.ALL | wx.ALIGN_RIGHT, 5)
        return sizer
