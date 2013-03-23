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
from wx.lib.scrolledpanel import ScrolledPanel
import genicontrol.dataitems as dataitems
from genicontrol.model.config import DataitemConfiguration
import genicontrol.controlids as controlids


class ParamPanel(ScrolledPanel):
    def __init__(self, parent):
        ScrolledPanel.__init__(self, parent = parent, id = wx.ID_ANY)

        sizer = self.addValues()
        self.btnParameters = wx.Button(self, label = "Set Parameters", id = controlids.ID_SET_REFERENCE_VALUES)

        sizer.Add(self.btnParameters, ((len(DataitemConfiguration['Parameters']) + 1), 0), wx.DefaultSpan, wx.ALL | wx.ALIGN_LEFT, 5)

        self.SetSizerAndFit(sizer)
        self.SetupScrolling()

    def choiceButton(self, event):
        self.setControlMode(event.EventObject.controlMode)

    def addValues(self):
        sizer = wx.GridBagSizer(5, 45)
        for idx, item in enumerate(DataitemConfiguration['Parameters']):
            key, displayName, unit, controlID = item
            ditem =  dataitems.PARAMETER[key]

            ctrl = wx.StaticText(self, wx.ID_ANY, displayName, style = wx.ALIGN_RIGHT)
            ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 0), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.TextCtrl(self, controlID, "n/a", style = wx.ALIGN_RIGHT)
            ctrl.Enable(False)
            ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 1), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.StaticText(self, wx.ID_ANY, unit, style = wx.ALIGN_LEFT)
            sizer.Add(ctrl, (idx, 2), wx.DefaultSpan, wx.ALL | wx.ALIGN_LEFT, 5)
        return sizer

