#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2016 by Christoph Schueler <github.com/Christoph2,
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

import array
import logging
import os
import sys

# Allow starting the program directly ('python3 GeniControl.py' inside tools/genicontrol):
# the packages 'genicontrol' and 'genilib' live in the parent directory.
_TOOLS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)

import queue
import wx
from genilib.pubsub import pub as Publisher
from wx import CallAfter
import time
import threading
from genicontrol.view.mcpanel import MCPanel
from genicontrol.view.infopanel import InfoPanel
from genicontrol.view.refpanel import RefPanel
from genicontrol.view.parampanel import ParamPanel
from genicontrol.model.NullModel import NullModel
from genicontrol.model.config import DataitemConfiguration
from genicontrol.controller.GUIController import GUIController
import genicontrol.controlids as controlids
import genicontrol.defs as defs
from genilib.configuration import Config
from genicontrol.view.options import showOptionsDialogue
from genilib.gui.menu import Menu, MenuItem, MenuSeparator, createMenuBar
from genilib.utils import dumpHex

TR = wx.GetTranslation

class BusmonitorPanel(wx.Panel):
    def __init__(self, parent):
        self.config = Config("GeniControl")
        self.logfilewanted = self.config.get('general', 'logfilewanted')
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)
        sizer = wx.BoxSizer()
        font = wx.Font(10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.tc = wx.TextCtrl(self, wx.NewId(), style = wx.TE_MULTILINE | wx.HSCROLL | wx.TE_RICH2 | wx.TE_NOHIDESEL | wx.TE_READONLY)
        self.tc.SetFont(font)
        sizer.Add(self.tc, 1, wx.EXPAND | wx.GROW)
        self.SetSizerAndFit(sizer)
        self.logFile =  None
        if self.logfilewanted == '1':
            self.logFile =  open(os.path.join(defs.CONFIGURATION_DIRECTORY, 'busmonitor.log'), 'w')

    def __del__(self):
        if self.logFile:
            self.logFile.close()

    def formatTelegram(self, rxTx, telegram):
        timestamp = time.strftime("%d/%b/%Y %H:%M:%S")
        rt = "Rx" if rxTx else "Tx"
        if not isinstance(telegram, (list, tuple, array.array)):
            #print("WARNING '%s' isn't a correct telegram!")
            return "[%s] %s - INVALID!\n"  % (timestamp, rt, )
        formattedTelegram = ' '.join(["0x%02x" % x for x in telegram])
        return "[%s] %s - %s\n" % (timestamp, rt, formattedTelegram)

    def appendLine(self, rxTx, telegram):
        formattedTelegram = self.formatTelegram(rxTx, telegram)
        self.tc.AppendText(formattedTelegram)
        if self.logFile:
            self.logFile.write(formattedTelegram)

class TestNB(wx.Notebook):
    def __init__(self, parent, id):
        wx.Notebook.__init__(self, parent, id, size = (21, 21), style = wx.BK_DEFAULT | wx.BK_BOTTOM)
        self.mcPanel = MCPanel(self)
        self.AddPage(self.mcPanel, "Measurement + Control")
        self.bmPanel = BusmonitorPanel(self)
        self.AddPage(self.bmPanel, "Busmonitor")
        self.refPanel = RefPanel(self)
        self.AddPage(self.refPanel, "References")
        self.paramPanel = ParamPanel(self)
        self.AddPage(self.paramPanel, "Parameters")
        self.infoPanel = InfoPanel(self)
        self.AddPage(self.infoPanel, "Info")


class GBFrame(wx.Frame):
    def __init__(self, parent, menuData, size = None, pos = None):
        wx.Frame.__init__(self, parent, -1, "GeniControl", size = size, pos = pos)
        self.initStatusBar()
        createMenuBar(self, menuData)
        self.locale = None
        #self.updateLanguage(wx.LANGUAGE_ITALIAN)

##
##        self.log = wx.TextCtrl(self, -1, style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
##        if wx.Platform == "__WXMAC__":
##            self.log.MacCheckSpelling(False)
##

        # Set the wxWindows log target to be this textctrl
        #wx.Log.SetActiveTarget(wx.LogTextCtrl(self.log))

        # for serious debugging
        wx.Log.SetActiveTarget(wx.LogStderr())
        #wx.Log_SetTraceMask(wx.TraceMessages

        self.notebook = TestNB(self, wx.ID_ANY)
        # wxPython 4/GTK3: let a sizer manage the notebook, and make sure the
        # window is at least as large as its content (otherwise the tabs are cut off).
        frameSizer = wx.BoxSizer(wx.VERTICAL)
        frameSizer.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(frameSizer)
        # Size needed by the main page (the Info grid scrolls, so it is not considered).
        nb = self.notebook
        pages = [nb.GetPage(i).GetBestSize() for i in range(nb.GetPageCount())]
        nbBest = nb.GetBestSize()
        overhead = wx.Size(nbBest.width - max(p.width for p in pages), nbBest.height - max(p.height for p in pages))
        pageSize = nb.mcPanel.GetBestSize()
        needed = self.ClientToWindowSize(wx.Size(pageSize.width + overhead.width, pageSize.height + overhead.height))
        area = wx.Display(0).GetClientArea()
        width = min(max(size.width if size else 0, needed.width), area.width)
        height = min(max(size.height if size else 0, needed.height), area.height)
        self.SetSize(wx.Size(width, height))
        self.Layout()
        if not pos:
            self.Center()

    def initialize(self, model, quitEvent):
        self._model = model
        self.setPumpOnline(False, initial = True)
        self._quitEvent = quitEvent
        self._messageQueue = queue.Queue()

    def quit(self):
        pass

    def setPumpOnline(self, online, initial = False):
        mc = self.notebook.mcPanel
        if online:
            self.SetStatusText("Pump connected", 0)
        else:
            self.SetStatusText("Waiting for pump..." if initial else "NO REPLY FROM PUMP", 0)
            mc.setOffline()

    def post(self, category, message):
        self._messageQueue.put_nowait((category, message))

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

    def onSaveSettings(self, event): pass
    def onSaveSnapShot(self, event): pass
    def onSaveParameter(self, event): pass
    def onSaveInfo(self, event): pass
    def onLoadParamter(self, event): pass

    def onOptions(self, event):
        showOptionsDialogue(self)

    def onCloseWindow(self, event):
        Publisher.sendMessage('QUIT')

    def shutdownView(self):
        self.quit()
        self.saveConfiguration()
        self.Destroy()

    def saveConfiguration(self):
        size = self.Size
        pos = self.Position
        config = Config("GeniControl")
        config.set('window', 'posx', pos.x)
        config.set('window', 'posy', pos.y)
        config.set('window', 'sizex', size.x)
        config.set('window', 'sizey', size.y)

    def updateBusmonitor(self, rxTx, telegram):
        self.notebook.bmPanel.appendLine(rxTx, telegram)


class GeniControlApp(wx.App):
    def __init__(self):
        super(GeniControlApp, self).__init__()

MAIN_MENU = (
    Menu("&File",
         MenuItem("&Save", "Save settings.", "onSaveSettings"),
         MenuItem("Save &parameter", "", "onSaveParameter"),
         MenuItem("Save &info", "Save parameter scaling information to a file.", "onSaveInfo"),
         MenuItem("&Load paramter", "", "onLoadParamter"),
         MenuSeparator(),
         MenuItem("&Exit", "Exit GeniControl", "onCloseWindow")),

    Menu("&Extras", MenuItem("&Options", "", "onOptions"))
)

def main():
    logger = logging.getLogger("GeniControl")
    config = Config("GeniControl")
    config.load()
    size = wx.Size(config.get('window', 'sizex'), config.get('window', 'sizey'))
    pos = wx.Point(config.get('window', 'posx'), config.get('window', 'posy'))
    app = GeniControlApp()
    # wxPython >= 4.1 turns some harmless legacy sizer-flag combinations into errors.
    if hasattr(wx, 'SizerFlags') and hasattr(wx.SizerFlags, 'DisableConsistencyChecks'):
        wx.SizerFlags.DisableConsistencyChecks()
    frame = GBFrame(None, MAIN_MENU, size, pos)

    controller = GUIController(NullModel, frame)

    frame.Show(True)
    app.MainLoop()
    config.save()

if __name__ == '__main__':
    main()

