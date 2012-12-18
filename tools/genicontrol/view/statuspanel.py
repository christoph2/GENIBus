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
from genicontrol.model.config import DataitemConfiguration
import genicontrol.dataitems as dataitems

class StatusPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)
        sizer = self.addValues()
        ctrl = wx.StaticText(self, wx.ID_ANY, 'Performance', style = wx.ALIGN_RIGHT)
        sizer.Add(ctrl, (6, 0), wx.DefaultSpan, wx.ALL, 5)

        gauge = wx.Gauge(parent = self, range = 100)
        gauge.SetToolTip(wx.ToolTip('n/a'))
        gauge.SetValue(0)
        sizer.Add(gauge, (6, 1), (1, 1), wx.ALL, 5)

        ctrl = wx.StaticText(self, wx.ID_ANY, '%', style = wx.ALIGN_RIGHT)
        sizer.Add(ctrl, (6, 2), wx.DefaultSpan, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.SetSizer(sizer)

    def addValues(self):
        sizer = wx.GridBagSizer(5, 45)
        for idx, item in enumerate(DataitemConfiguration['MeasurementValues']):
            key, displayName, unit = item
            ditem =  dataitems.MEASUREMENT_VALUES[key]

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

