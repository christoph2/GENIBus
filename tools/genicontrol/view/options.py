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
from wx.lib.masked import ipaddrctrl
from wx.lib.masked import TextCtrl
from genicontrol.config import Config

ID_IPADDR   = wx.NewId()
ID_PORT     = wx.NewId()

class Options(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, u'Options')

        sizer = wx.BoxSizer(wx.VERTICAL)
        gridsizer = wx.FlexGridSizer(2,2)
        st = wx.StaticText(self, label = 'Server IP-address')
        gridsizer.Add(st, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        addr = ipaddrctrl.IpAddrCtrl(self, id = ID_IPADDR)
        gridsizer.Add(addr, 1, wx.ALL | wx.ALIGN_RIGHT, 5)
        st = wx.StaticText(self, label = 'Server-port')
        gridsizer.Add(st, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        tc = TextCtrl(self, mask = '#####')
        gridsizer.Add(tc, 1, wx.ALL | wx.ALIGN_RIGHT, 5)
        sizer.Add(gridsizer, 1, wx.ALL, 5)
        line = wx.StaticLine(self, style = wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)
        btnsizer = wx.StdDialogButtonSizer()
        okButton = wx.Button(self, id = wx.ID_OK)
        okButton.SetDefault()
        btnsizer.Add(okButton)
        cancelButton = wx.Button(self, id = wx.ID_CANCEL)
        btnsizer.AddButton(cancelButton)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)

        addr.SetFocus()
        #self.SetValues()
        self.Centre()
        retval = self.ShowModal()
        retval = wx.ID_OK
        if retval == wx.ID_OK:
            pass # TODO: Save Config!!!
        self.Destroy()


def showOptionsDialogue(parent):
    options = Options(parent)

def testDialogue():
    showOptionsDialogue(None)


def main():
    class TestApp(wx.PySimpleApp):
        def __init__(self):
            super(TestApp, self).__init__()

    app = TestApp()
    testDialogue()

if __name__ == '__main__':
    main()

