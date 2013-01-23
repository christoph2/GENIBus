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
from genicontrol.configuration import Config

ID_IPADDR   = wx.NewId()
ID_SUBNET   = wx.NewId()
ID_PORT     = wx.NewId()
ID_POLL     = wx.NewId()


def fixIP(addr):
    return '.'.join(["%3s" % j for j in [i.strip() for i in addr.split('.')]])

class Options(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, u'Options')
        config = Config()
        #config.loadConfiguration()

        sizer = wx.BoxSizer(wx.VERTICAL)
        gridsizer = wx.FlexGridSizer(4,2)
        st = wx.StaticText(self, label = 'Server IP-address')
        gridsizer.Add(st, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        addr = ipaddrctrl.IpAddrCtrl(self, id = ID_IPADDR)
        gridsizer.Add(addr, 1, wx.ALL | wx.ALIGN_RIGHT, 5)
        st = wx.StaticText(self, label = 'Subnet-mask')
        gridsizer.Add(st, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        mask = ipaddrctrl.IpAddrCtrl(self, id = ID_SUBNET)
        gridsizer.Add(mask, 1, wx.ALL | wx.ALIGN_RIGHT, 5)
        st = wx.StaticText(self, label = 'Server-port')
        gridsizer.Add(st, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        port = TextCtrl(self, id = ID_PORT, mask = '#####')
        gridsizer.Add(port, 1, wx.ALL | wx.ALIGN_RIGHT, 5)
        sizer.Add(gridsizer, 1, wx.ALL, 5)
        st = wx.StaticText(self, label = 'Polling interval')
        gridsizer.Add(st, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        poll = TextCtrl(self, id = ID_POLL, mask = '#####')
        gridsizer.Add(poll, 1, wx.ALL | wx.ALIGN_RIGHT, 5)
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
	config.serverIP = fixIP(config.serverIP)
        addr.SetValue(config.serverIP)
        mask.SetValue(config.subnetMask)
        port.SetValue(config.serverPort)
        poll.SetValue(str(config.pollingInterval))

        addr.SetFocus()
        #self.SetValues()
        self.Centre()
        retval = self.ShowModal()
        retval = wx.ID_OK
        if retval == wx.ID_OK:
	    config.serverIP = fixIP(addr.GetValue())
            config.subnetMaskP = mask.GetValue()
            config.serverPortP = port.GetValue()
            config.pollingInterval = poll.GetValue()
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

