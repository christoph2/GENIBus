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


class OptionsView(wx.Dialog):
    def __init__(self, parent, controller, model):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, u'Options')
        self.tcpControls = []
        self.serialControls = []
        self.simControls = []
        self.controller = controller
        self.model = model
        #self.model.registerObserver(self)

    def createControls(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        gridsizer = wx.FlexGridSizer(3 ,2)

        staticBox = wx.StaticBoxSizer(wx.StaticBox(self, -1, " Driver " ), wx.VERTICAL )

        self.radioTcp = wx.RadioButton(self, ID_RB_TCPIP, " Arduino / TCP ", style = wx.RB_GROUP)
        gridsizer.Add(self.radioTcp, 1, wx.ALL, 5)
        gridsizer2 = wx.FlexGridSizer(3 ,2)

        st = wx.StaticText(self, label = 'Server IP-address')
        gridsizer2.Add(st, 1, wx.ALL | wx.ALIGN_LEFT, 5)

        self.addr = ipaddrctrl.IpAddrCtrl(self, id = ID_IPADDR)
        self.tcpControls.append(self.addr)

        gridsizer2.Add(self.addr, 1, wx.ALL | wx.ALIGN_RIGHT, 5)
        st = wx.StaticText(self, label = 'Subnet-mask')

        gridsizer2.Add(st, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        self.mask = ipaddrctrl.IpAddrCtrl(self, id = ID_SUBNET)
        self.tcpControls.append(self.mask)

        gridsizer2.Add(self.mask, 1, wx.ALL | wx.ALIGN_RIGHT, 5)
        st = wx.StaticText(self, label = 'Server-port')

        gridsizer2.Add(st, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        self.port = TextCtrl(self, id = ID_PORT, mask = '#####')
        self.tcpControls.append(self.port)

        gridsizer2.Add(self.port, 1, wx.ALL | wx.ALIGN_RIGHT, 5)
        gridsizer.Add(gridsizer2, 1, wx.ALL | wx.ALIGN_TOP, 5)

        self.radioSerial = wx.RadioButton(self, ID_RB_SERIAL, " Serial Port ")
        gridsizer.Add(self.radioSerial, 1, wx.ALL, 5)

        boxSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        st = wx.StaticText(self, label = 'Port')
        boxSizer3.Add(st, 1, wx.ALL, 5)

        self.serialPort = TextCtrl(self, id = ID_SERIAL_PORT)
        self.serialControls.append(self.serialPort)
        boxSizer3.Add(self.serialPort, 1, wx.ALL, 5)
        gridsizer.Add(boxSizer3, 1, wx.ALL, 5)

        self.radioSim = wx.RadioButton(self, ID_RB_SIM, " Simulator ")
        gridsizer.Add(self.radioSim, 1, wx.ALL, 5)

        st = wx.StaticText(self, label = '')
        gridsizer.Add(st, 1, wx.ALL, 5)

        staticBox.Add(gridsizer)
        sizer.Add(staticBox, 1, wx.ALL, 5)

        boxSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        st = wx.StaticText(self, label = 'Polling interval')

        boxSizer2.Add(st, 1, wx.ALL | wx.ALIGN_LEFT, 5)
        self.poll = TextCtrl(self, id = ID_POLL, mask = '#####')

        boxSizer2.Add(self.poll, 1, wx.ALL | wx.ALIGN_RIGHT, 5)
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

        self.Bind(wx.EVT_RADIOBUTTON, self.onDriverSelected, self.radioTcp)
        self.Bind(wx.EVT_RADIOBUTTON, self.onDriverSelected, self.radioSerial)
        self.Bind(wx.EVT_RADIOBUTTON, self.onDriverSelected, self.radioSim)

        self.SetSizerAndFit(sizer)

    def setInitialValues(self):
        self.addr.SetValue(self.model.getServerIP())
        self.mask.SetValue(self.model.getSubnetMask())
        self.port.SetValue(self.model.getServerPort())
        self.poll.SetValue(self.model.getPollingInterval())
        self.serialPort.SetValue(self.model.getSerialPort())
        self.driver = self.model.getNetworkDriver()
        if self.driver == 0:
            value = 'Simulator'
            button = self.radioSim
        elif self.driver == 1:
            value = 'Arduino / TCP'
            button = self.radioTcp
        elif self.driver == 2:
            value = 'Serial'
            button = self.radioSerial
        button.SetValue(True)
        self.enableRadioButton(button.GetId())

    def show(self):
        self.Centre()
        return self.ShowModal()

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


class OptionsModel(object):

    def __init__(self):
        self.config = Config("GeniControl")

    def initialize(self):
        pass

    def load(self):
        self.config.load()
        self.driver = self.config.get('network', 'driver')
        self.serverIP = fixIP(self.config.get('network', 'serverip'))
        self.subnetMask = fixIP(self.config.get('network', 'subnetmask'))
        self.serverport = str(self.config.get('network', 'serverport'))
        self.pollinginterval = str(self.config.get('general', 'pollinginterval'))
        self.serialPort = self.config.get('serial', 'serialport')

    def save(self):
        pass

    def getNetworkDriver(self):
        return self.driver

    def getServerIP(self):
        return self.serverIP

    def getSubnetMask(self):
        return self.subnetMask

    def getServerPort(self):
        return self.serverport

    def getPollingInterval(self):
        return self.pollinginterval

    def getSerialPort(self):
        return self.serialPort

    def setNetworkDriver(self, value):
        self.config.set('network', 'driver', value)

    def setServerIP(self, value):
        self.config.set('network', 'serverip', fixIP(value))

    def setSubnetMask(self, value):
        self.config.set('network', 'subnetmask', fixIP(value))

    def setServerPort(self, value):
        self.config.set('network', 'serverport',  value)

    def setPollingInterval(self, value):
        self.config.set('general', 'pollinginterval', value)

    def setSerialPort(self, value):
        self.config.set('serial', 'serialport', value)


class OptionsController(object):

    def __init__(self, parent, model):
        self.model = model
        self.view = OptionsView(parent, self, model)
        self.model.initialize()
        self.model.load()
        self.view.createControls()
        self.view.setInitialValues()

    def execute(self):
        # Disable/Enable Controls.
        result = self.view.show()
        if result == wx.ID_OK:
            #self.model.save()
            self.model.setServerIP(self.view.addr.GetValue())
            self.model.setSubnetMask(self.view.mask.GetValue())
            self.model.setServerPort(self.view.port.GetValue())
            self.model.setPollingInterval(self.view.poll.GetValue())
            self.model.setNetworkDriver(self.view.driver)
            self.model.setSerialPort(self.view.serialPort.GetValue())

        else:
            pass
        self.view.Destroy()


def showOptionsDialogue(parent):
    model = OptionsModel()
    controller = OptionsController(parent, model)
    controller.execute()


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

