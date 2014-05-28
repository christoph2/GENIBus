#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2014 by Christoph Schueler <github.com/Christoph2,
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
from genicontrol.serialport import serialAvailable
from genilib.configuration import Config

ID_IPADDR       = wx.NewId()
ID_SUBNET       = wx.NewId()
ID_PORT         = wx.NewId()
ID_POLL         = wx.NewId()
ID_SERIAL_PORT  = wx.NewId()

ID_RB_TCPIP     = wx.NewId()
ID_RB_SERIAL    = wx.NewId()
ID_RB_SIM       = wx.NewId()


def fixIP(addr):
    return '.'.join(["%3s" % j for j in [i.strip() for i in addr.split('.')]])

class Options(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, u'Options')
        self.tcpControls = []
        self.serialControls = []
        self.simControls = []

        config = Config()
        config.load()

        self.driver = config.get('network', 'driver')

        sizer = wx.BoxSizer(wx.VERTICAL)

        gridsizer = wx.FlexGridSizer(3 ,2)

        staticBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, " Driver " ), wx.VERTICAL )

        radioTcp = wx.RadioButton(self, ID_RB_TCPIP, " Arduino / TCP ", style = wx.RB_GROUP)
        gridsizer.Add(radioTcp, 1, wx.ALL, 5)
        gridsizer2 = wx.FlexGridSizer(3 ,2)

        st = wx.StaticText(self, label = 'Server IP-address')
        gridsizer2.Add(st, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        addr = ipaddrctrl.IpAddrCtrl(self, id = ID_IPADDR)
        self.tcpControls.append(addr)
        gridsizer2.Add(addr, 1, wx.ALL | wx.ALIGN_RIGHT, 5)
        st = wx.StaticText(self, label = 'Subnet-mask')
        gridsizer2.Add(st, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        mask = ipaddrctrl.IpAddrCtrl(self, id = ID_SUBNET)
        self.tcpControls.append(mask)
        gridsizer2.Add(mask, 1, wx.ALL | wx.ALIGN_RIGHT, 5)
        st = wx.StaticText(self, label = 'Server-port')
        gridsizer2.Add(st, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        port = TextCtrl(self, id = ID_PORT, mask = '#####')
        self.tcpControls.append(port)
        gridsizer2.Add(port, 1, wx.ALL | wx.ALIGN_RIGHT, 5)
        gridsizer.Add(gridsizer2, 1, wx.ALL | wx.ALIGN_TOP, 5)

        radioSerial = wx.RadioButton(self, ID_RB_SERIAL, " Serial Port ")
        gridsizer.Add(radioSerial, 1, wx.ALL, 5)

        boxSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        st = wx.StaticText(self, label = 'Port')
        boxSizer3.Add(st, 1, wx.ALL, 5)
        serialPort = TextCtrl(self, id = ID_SERIAL_PORT)
        self.serialControls.append(serialPort)
        boxSizer3.Add(serialPort, 1, wx.ALL, 5)

        gridsizer.Add(boxSizer3, 1, wx.ALL, 5)

        radioSim = wx.RadioButton(self, ID_RB_SIM, " Simulator ")
        gridsizer.Add(radioSim, 1, wx.ALL, 5)
        st = wx.StaticText(self, label = '')
        gridsizer.Add(st, 1, wx.ALL, 5)

        staticBox.Add(gridsizer)
        sizer.Add(staticBox, 1, wx.ALL, 5)

        boxSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        st = wx.StaticText(self, label = 'Polling interval')
        boxSizer2.Add(st, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        poll = TextCtrl(self, id = ID_POLL, mask = '#####')
        boxSizer2.Add(poll, 1, wx.ALL | wx.ALIGN_RIGHT, 5)
        sizer.Add(boxSizer2)

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

        if not serialAvailable:
            radioSerial.Enable(False)

        self.Bind(wx.EVT_RADIOBUTTON, self.onDriverSelected, radioTcp)
        self.Bind(wx.EVT_RADIOBUTTON, self.onDriverSelected, radioSerial)
        self.Bind(wx.EVT_RADIOBUTTON, self.onDriverSelected, radioSim)

        self.SetSizerAndFit(sizer)

        serverIP = fixIP(config.get('network', 'serverip'))
        addr.SetValue(serverIP)
        subnetMask = fixIP(config.get('network', 'subnetmask'))
        mask.SetValue(subnetMask)
        port.SetValue(str(config.get('network', 'serverport')))
        poll.SetValue(str(config.get('general', 'pollinginterval')))
        serialPort.SetValue(str(config.get('serial', 'serialport')))
        if self.driver == 0:
            value = 'Simulator'
            button = radioSim
        elif self.driver == 1:
            value = 'Arduino / TCP'
            button = radioTcp
        elif self.driver == 2:
            value = 'Serial'
            button = radioSerial

        button.SetValue(True)
        self.enableRadioButton(button.GetId())
        #addr.SetFocus()
        self.Centre()
        retval = self.ShowModal()
        retval = wx.ID_OK
        if retval == wx.ID_OK:
            config.set('network', 'serverip', fixIP(addr.GetValue()))
            config.set('network', 'subnetmask', fixIP(mask.GetValue()))
            config.set('network', 'serverport',  port.GetValue())
            config.set('general', 'pollinginterval',  poll.GetValue())
            config.set('network', 'driver', self.driver)
            config.set('serial', 'serialport', serialPort.GetValue())
        self.Destroy()

    def onDriverSelected(self, event):
        self.enableRadioButton(event.GetId())

    def enableRadioButton(self, controlId):
        if controlId == ID_RB_TCPIP:
            self.enableTcpControls(True)
            self.enableSerialControls(False)
            self.enableSimControls(False)
            self.driver = 1
        elif controlId == ID_RB_SERIAL:
            self.enableTcpControls(False)
            self.enableSerialControls(True)
            self.enableSimControls(False)
            self.driver = 2
        elif controlId == ID_RB_SIM:
            self.enableTcpControls(False)
            self.enableSerialControls(False)
            self.enableSimControls(True)
            self.driver = 0

    def enableControls(self, controls, enable):
        for control in controls:
            control.Enable(enable)

    def enableTcpControls(self, enable):
        self.enableControls(self.tcpControls, enable)

    def enableSerialControls(self, enable):
        self.enableControls(self.serialControls, enable)

    def enableSimControls(self, enable):
        self.enableControls(self.simControls, enable)


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

