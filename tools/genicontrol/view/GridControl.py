#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

