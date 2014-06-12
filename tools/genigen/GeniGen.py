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

from collections import namedtuple
import threading

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import itertools
import logging

import wx
from wx.lib.scrolledpanel import ScrolledPanel
from genilib.configuration import Config as Config
from genilib.configuration import readConfigFile
from genicontrol.defs import CLASS_CAPABILITIES, NICE_CLASS_NAMES, OS_GET, OS_SET, OS_INFO

from genilib.gui.menu import Menu, MenuItem, MenuSeparator, createMenuBar, getMenuItem
from genicontrol.dataitems import DATAITEMS


TR = wx.GetTranslation


AnnotatedItem = namedtuple('AnnotatedItem', 'klass name capabilities items')


class Items(object): # NB: This class certainly doesn't belong here, but for now...
    _lock = threading.Lock()
    _items = dict()
    _classes = list()

    def __new__(cls):
        # Double-Checked Locking
        if not hasattr(cls, '_instance'):
            try:
                cls._lock.acquire()
                if not hasattr(cls, '_instance'):
                    cls._instance = super(cls.__class__, cls).__new__(cls)

                    for klass, items in itertools.groupby(DATAITEMS, lambda k: k.klass):
                        cls._classes.append(klass)
                        cls._items[klass] = AnnotatedItem(
                            klass, NICE_CLASS_NAMES[klass], CLASS_CAPABILITIES[klass],
                            list(sorted(items, key = lambda k: k.id))
                        )

            finally:
                cls._lock.release()
        return cls._instance

    @property
    def classes(self):
        return self._classes

    def itemsForClass(self, klass):
        return self._items.get(klass, [])

MY_MENU = (
Menu("&File",
    MenuItem("&Save\tCtrl-S", "Save setting.", "onSaveSettings"),
    MenuItem("Save &parameter", "", "onSaveParameter"),
    MenuItem("Save &info", "Save parameter scaling information to a file.", "onSaveInfo"),
    MenuItem("&Load paramter\tCtrl-L", "", "onLoadParamter"),
    MenuSeparator(),
    MenuItem("&Exit\tAlt-F4", "Exit GeniControl", "onCloseWindow")),

    Menu("&Extras", MenuItem("&Options", "", "onOptions"), Menu("SubMenu", MenuItem("Hello","", "onOptions")))
)


Control = namedtuple('Control', 'type item')


class ClassPanel(ScrolledPanel):
    def __init__(self, parent, root):
        ScrolledPanel.__init__(self, parent = parent, id = wx.ID_ANY)

        self.model = parent.model # Create a reference to model.

        numberOfItems = len(root.items)
        get = OS_GET in root.capabilities
        set = OS_SET in root.capabilities
        info = OS_INFO in root.capabilities
        #print "Number of Item in '%s' panel: %u" % (root.name, len(root.items))

        self.controlMap = {}

        sizer = wx.GridBagSizer(2, 2 + numberOfItems)
        self.addLabels(sizer, "Get", "Set", "Info")
        for idx, item in enumerate(root.items, 2):
            st = wx.StaticText(self, label = item.name)
            sizer.Add(st, (idx, 0), wx.DefaultSpan, wx.ALL, 5)
            st.SetToolTip(wx.ToolTip(item.note))
            if get:
                newId = self.addCheckBox(sizer, idx, 1)
                self.controlMap[newId] = Control(OS_GET, item)
            if set:
                newId = self.addCheckBox(sizer, idx, 2)
                self.controlMap[newId] = Control(OS_SET, item)
            if info:
                newId = self.addCheckBox(sizer, idx, 3)
                self.controlMap[newId] = Control(OS_INFO, item)

        self.SetSizerAndFit(sizer)
        self.SetupScrolling()

    def addRow(self, *items):
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        for item in items:
            sizer.Add(item, 1, wx.ALL, 5)

        return sizer

    def addCheckBox(self, sizer, row, column):
        cbId = wx.NewId()
        cb = wx.CheckBox(parent = self, id = cbId)
        sizer.Add(cb, (row, column), wx.DefaultSpan, wx.ALL, 5)
        cb.Bind(wx.EVT_CHECKBOX, self.onChecked)
        return cbId

    def addLabels(self, sizer, *labels):
        for idx, label in enumerate(labels, 1):
            sizer.Add(wx.StaticText(self, label = label), (0, idx), wx.DefaultSpan, wx.ALL, 5)

        sizer.Add(wx.StaticLine(self, style = wx.LI_HORIZONTAL), pos = (1, 0), span = (1, 4), flag = wx.ALL, border = -1)

    def onChecked(self, event):
        control = self.controlMap[event.GetId()]
        state = event.IsChecked()
        self.model.update(control.type, control.item.name, state)



class ItemsNotebook(wx.Notebook):
    def __init__(self, parent, id):
        wx.Notebook.__init__(self, parent, id, size = (21, 21), style = wx.BK_DEFAULT | wx.BK_BOTTOM)

        self.model = parent.model # Create a reference to model.

        self.pages = []
        for cls in self.model.classes:
            root = self.model.itemsForClass(cls)
            self.pages.append(self.AddPage(ClassPanel(self, root), root.name))


class GeniGenFrame(wx.Frame):
    def __init__(self, parent, size = None, pos = None):
        wx.Frame.__init__(self, parent, -1, "GeniGen", size = size, pos = pos)
        self.initStatusBar()
        createMenuBar(self, MY_MENU)
        self.locale = None
        self.model = GeniGenModel() # Just Model-View for now...
        self.notebook = ItemsNotebook(self, wx.NewId())

    def initStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1, -2, -3])

    def onCloseWindow(self, event):
        self.Destroy()

    def onOptions(self, event):
        item = getMenuItem(self, event)
        itemID = item.GetId()
        print itemID, event.Id

    def onSaveSettings(self, event):
        item = getMenuItem(self, event)
        itemID = item.GetId()
        print itemID, event.Id

    def onSaveParameter(self, event):
        item = getMenuItem(self, event)
        itemID = item.GetId()
        print itemID, event.Id

    def onSaveInfo(self, event):
        pass

    def onLoadParamter(self, event):
        pass


class GeniGenModel(object):
    TYPE_MAP = {
        0: "Get",
        2: "Set",
        3: "Info",
    }

    def __init__(self):
        self.items = Items()

    def update(self, type_, name, state):
        print "Control: %s type: %s state: %s" % (name, self.TYPE_MAP[type_], "On" if state else "Off")

    # Delegate the following two methods.
    @property
    def classes(self):
        return iter(self.items.classes)

    def itemsForClass(self, klass):
        return self.items.itemsForClass(klass)


class GeniGenApp(wx.PySimpleApp):
    def __init__(self):
        super(GeniGenApp, self).__init__()

def main():
    logger = logging.getLogger("GeniGen")
    config = Config("GeniGen")
    config.load()
    size = wx.Size(config.get('window', 'sizex'), config.get('window', 'sizey'))
    pos = wx.Point(config.get('window', 'posx'), config.get('window', 'posy'))
    app = GeniGenApp()
    frame = GeniGenFrame(None, size, pos)

    #controller = GUIController(NullModel, frame)

    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()

