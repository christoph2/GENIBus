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

class StatusPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)

        staticBox = wx.StaticBox(self, label = 'Pump status')
        groupSizer = wx.StaticBoxSizer(staticBox)

        sizer = self.addValues()
        ctrl = wx.StaticText(self, wx.ID_ANY, 'Performance', style = wx.ALIGN_RIGHT)
        sizer.Add(ctrl, (6, 0), wx.DefaultSpan, wx.ALL, 5)

        gauge = wx.Gauge(parent = self, range = 100)
        gauge.SetToolTip(wx.ToolTip('n/a'))
        gauge.SetValue(0)
        sizer.Add(gauge, (6, 1), (1, 1), wx.ALL, 5)

        ctrl = wx.StaticText(self, wx.ID_ANY, '%', style = wx.ALIGN_RIGHT)
        sizer.Add(ctrl, (6, 2), wx.DefaultSpan, wx.ALL | wx.ALIGN_RIGHT, 5)

        groupSizer.Add(sizer)
        self.SetSizerAndFit(groupSizer)

    def addValues(self):
        sizer = wx.GridBagSizer(5, 45)
        for idx, item in enumerate(DataitemConfiguration['MeasurementValues']):
            key, displayName, unit, controlID = item
            ditem =  dataitems.MEASUREMENT_VALUES[key]
            if key == 'f_act':
                continue

            ctrl = wx.StaticText(self, wx.ID_ANY, displayName, style = wx.ALIGN_RIGHT)
            ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 0), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.TextCtrl(self, wx.ID_ANY, "n/a", style = wx.ALIGN_RIGHT)
            ctrl.Enable(False)
            ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 1), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.StaticText(self, wx.ID_ANY, unit, style = wx.ALIGN_RIGHT)
            sizer.Add(ctrl, (idx, 2), wx.DefaultSpan, wx.ALL | wx.ALIGN_RIGHT, 5)
        return sizer


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

