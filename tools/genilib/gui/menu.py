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

__all__ = ['createMenuBar']

import wx

class Item(object):

    def __init__(self, name):
        self.name = name


class Menu(Item):

    def __init__(self, name, *items):
        super(Menu, self).__init__(name)
        self.items = []

        for item in items:
            assert isinstance(item, Item)
            self.items.append(item)

    def add(self, item):
        self.items.append(item)

    def __str__(self):
        return "< MENU: '%s' %s" % (self.name, self.items)

    __repr__ = __str__


class MenuItem(Item):

    def __init__(self, name, helpString, action,  kind = wx.ITEM_NORMAL):
        super(MenuItem, self).__init__(name)
        self.helpString = helpString
        self.action = action
        self.kind = kind

    def __str__(self):
        return "< MenuItem: '%s' >" % (self.name, )

    __repr__ = __str__


class MenuSeparator(MenuItem):

    def __init__(self):
        super(MenuSeparator, self).__init__('', '', None)

    def __str__(self):
        return "< SEPARATOR >"

    __repr__ = __str__


def createItem(window, menu, item):
    print "[%s]" % item.name

    if isinstance(item, MenuSeparator):
        menu.AppendSeparator()
    else:
        menuItem = wx.MenuItem(menu, -1, item.name, item.helpString, item.kind)
        menu.AppendItem(menuItem)
        actionHandler = getattr(window, item.action.strip())
        window.Bind(wx.EVT_MENU, actionHandler, menuItem)

def appendItems(window, menu, menuData):
    for item in menuData.items:
        if isinstance(item, Menu):
            createSubMenu(window, menu, item)
        else:
            createItem(window, menu, item)


def createSubMenu(window, menu, menuData):
    submenu = wx.Menu()
    menu.AppendMenu(-1, menuData.name, submenu)
    appendItems(window, submenu, menuData)


def createMenu(window, menuBar, menuData):
    menu = wx.Menu()
    menuBar.Append(menu, menuData.name)
    appendItems(window, menu, menuData)


def createMenuBar(window, menuData):
    menuBar = wx.MenuBar()
    for menu in menuData:
        createMenu(window, menuBar, menu)
    window.SetMenuBar(menuBar)


