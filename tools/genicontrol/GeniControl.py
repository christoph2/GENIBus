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

import logging
import wx
import time
import threading
import genicontrol.dataitems as dataitems
from genicontrol.view.mcpanel import MCPanel
from genicontrol.view.infopanel import InfoPanel
from genicontrol.view.refpanel import RefPanel
from genicontrol.model.NullModel import NullModel
from genicontrol.model.config import DataitemConfiguration
from genicontrol.controller.GUIController import GUIController
import genicontrol.controlids as controlids
from genicontrol.configuration import Config as Config
from genicontrol.view.options import showOptionsDialogue

TR = wx.GetTranslation


class TabPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)

        sizer = wx.BoxSizer(wx.VERTICAL)
        txtOne = wx.TextCtrl(self, wx.ID_ANY, "")
        txtTwo = wx.TextCtrl(self, wx.ID_ANY, "")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(txtOne, 0, wx.ALL, 5)
        sizer.Add(txtTwo, 0, wx.ALL, 5)

        #sizer.Add(bmp, 0, wx.ALL, 5)

        self.SetSizer(sizer)


class BusmonitorPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)
        sizer = wx.BoxSizer()
        tc = wx.TextCtrl(self, wx.NewId(), style = wx.TE_MULTILINE | wx.HSCROLL | wx.TE_RICH2 | wx.TE_NOHIDESEL | wx.TE_READONLY)
        sizer.Add(tc, 1, wx.EXPAND | wx.GROW)
        self.SetSizerAndFit(sizer)


class TestNB(wx.Notebook):
    def __init__(self, parent, id):
        wx.Notebook.__init__(self, parent, id, size = (21, 21), style = wx.BK_DEFAULT | wx.BK_BOTTOM)
        tabOne = TabPanel(self)
        self.AddPage(MCPanel(self), "Measurement + Control")
        self.AddPage(BusmonitorPanel(self), "Busmonitor")
        self.AddPage(RefPanel(self), "References")
        self.AddPage(tabOne, "Parameters")
        self.AddPage(InfoPanel(self), "Info")


class GBFrame(wx.Frame):
    def __init__(self, parent, size = None, pos = None):
        wx.Frame.__init__(self, parent, -1, "GeniControl", size = size, pos = pos)
        self.initStatusBar()
        self.createMenuBar()
        self.locale = None
        #self.updateLanguage(wx.LANGUAGE_ITALIAN)

        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)

##
##        self.log = wx.TextCtrl(self, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
##        if wx.Platform == "__WXMAC__":
##            self.log.MacCheckSpelling(False)
##

        # Set the wxWindows log target to be this textctrl
        #wx.Log_SetActiveTarget(wx.LogTextCtrl(self.log))

        # for serious debugging
        wx.Log_SetActiveTarget(wx.LogStderr())
        #wx.Log_SetTraceMask(wx.TraceMessages

        self.notebook = TestNB(self, wx.NewId())
        if not pos:
            self.Center()
        wx.LogMessage("Started...")

    def initialize(self, quitEvent):
        self._quitEvent = quitEvent
        self._guiThread = GUIThread(None, self._quitEvent)
        self._guiThread.start()
        return self._guiThread

    def quit(self):
        self._quitEvent.set()
        self._guiThread.join()

    def updateLanguage(self, lang):
        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale

        # create a locale object for this language
        self.locale = wx.Locale(lang)
        if self.locale.IsOk():
            self.locale.AddCatalog('wxpydemo')
        else:
            self.locale = None

    def initStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1, -2, -3])

    def menuData(self):
        return [(TR("&File"), (
                    ("&Save snapshot", "Save current measurement values to a file.", self.onSaveSnapShot),
                    ("Save &parameter", "", self.onSaveParameter),
                    ("Save &info", "Save parameter scaling information to a file.", self.onSaveInfo),
                    ("&Load paramter", "", self.onLoadParamter),
                    ("", "", ""),
                    ("&Exit", "Exit GeniControl", self.onCloseWindow))),
                ("&Extras", (("&Options", "", self.onOptions),),),
                ]

    def createMenuBar(self):
        menuBar = wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1]
            menuBar.Append(self.createMenu(menuItems), menuLabel)
        self.SetMenuBar(menuBar)

    def createMenu(self, menuData):
        menu = wx.Menu()
        for eachItem in menuData:
            if len(eachItem) == 2:
                label = eachItem[0]
                subMenu = self.createMenu(eachItem[1])
                menu.AppendMenu(wx.NewId(), label, subMenu)
            else:
                self.createMenuItem(menu, *eachItem)
        return menu

    def createMenuItem(self, menu, label, status, handler,
                       kind=wx.ITEM_NORMAL):
        if not label:
            menu.AppendSeparator()
            return
        menuItem = menu.Append(-1, label, status, kind)
        self.Bind(wx.EVT_MENU, handler, menuItem)

    def onSaveSnapShot(self, event): pass
    def onSaveParameter(self, event): pass
    def onSaveInfo(self, event): pass
    def onLoadParamter(self, event): pass

    def onOptions(self, event):
        showOptionsDialogue(self)

    def onCloseWindow(self, event):
        wx.LogMessage("Exiting...")
        wx.LogMessage("%s %s" % (self.GetSize(), self.GetPosition()))
        self.quit()
        self.saveConfiguration()
        self.Destroy()

    def saveConfiguration(self):
        size = self.Size
        pos = self.Position
        config = Config()
        config.posX = pos.x
        config.posY = pos.y
        config.sizeX = size.x
        config.sizeY = size.y


class GUIThread(threading.Thread):
    logger = logging.getLogger("genicontrol")

    def __init__(self, model, quitEvent):
        super(GUIThread, self).__init__()
        self._model = model
        self.quitEvent = quitEvent

    def run(self):
        name = self.getName()
        print "Starting %s." % name
        while True:
            if self.quitEvent.isSet():
                break
            time.sleep(0.1)
        self.quitEvent.wait(0.5)
        print "Exiting %s." % name


class GeniControlApp(wx.PySimpleApp):
    def __init__(self):
        super(GeniControlApp, self).__init__()

def main():
    logger = logging.getLogger("genicontrol")
    config = Config()
    config.loadConfiguration()
    size = wx.Size(config.sizeX, config.sizeY)
    pos = wx.Point(config.posX, config.posY)
    app = GeniControlApp()
    frame = GBFrame(None, size, pos)

    controller = GUIController(NullModel, frame)

    frame.Show(True)
    app.MainLoop()
    config.saveConfiguration()

if __name__ == '__main__':
    main()

