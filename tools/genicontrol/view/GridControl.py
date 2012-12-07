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
from wx.lib.embeddedimage import PyEmbeddedImage
import wx.grid as gridlib
import wx.lib.mixins.grid as mixins
import wx.lib.mixins.listctrl as listmix

edir = lambda m, n: [ x for x in dir(m) if n.lower() in x.lower()]

class GridControl(gridlib.Grid, mixins.GridAutoEditMixin):
    def __init__(self, parent, values, items):
        gridlib.Grid.__init__(self, parent, -1, size = wx.DefaultSize)
        mixins.GridAutoEditMixin.__init__(self)
        self.moveTo = None

        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(gridlib.EVT_GRID_ROW_SIZE, self.OnRowSize)
        self.Bind(gridlib.EVT_GRID_COL_SIZE, self.OnColSize)

        self.CreateGrid(len(values), 8)

        fnt = self.GetFont()
        self.SetColLabelValue(0, "Dataitem")
        self.SetColLabelValue(1, "Unit")
        self.SetColLabelValue(2, "Zero")
        self.SetColLabelValue(3, "Range")

        for i in range((len(values))):
            self.SetCellValue(i, 0, values[i])
            self.SetCellValue(i, 1, 'n/a')
            self.SetCellValue(i, 2, 'n/a')
            self.SetCellValue(i, 3, 'n/a')
##            self.AutoSizeColumn(i)
##            self.SetCellValue(0, i, '')
##

        self.EnableEditing(False)

        self.Fit()
        self.Layout()
        self.SetAutoLayout(True)

        self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)
        self.SetRowLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)


    def OnIdle(self, evt):
        if self.moveTo != None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None
        evt.Skip()

    def OnRowSize(self, evt):
        evt.Skip()
        return

    def OnColSize(self, evt):
        evt.Skip()
        return

