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

__all__ = ['createMenuBar', 'getMenuItem', 'findMenuInMenuBar']

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

    def add(self, item):    # item can be MenuItem or Menu, e.g. Composite pattern.
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
    #print("[%s]" % item.name)

    if isinstance(item, MenuSeparator):
        menu.AppendSeparator()
    else:
        newID = wx.NewId()
        menuItem = wx.MenuItem(menu, newID, item.name, item.helpString, item.kind)
        item.id = newID
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
    newID = wx.NewId()
    menu.AppendMenu(newID, menuData.name, submenu)
    menuData.id = newID
    appendItems(window, submenu, menuData)


def createMenu(window, menuBar, menuData):
    menu = wx.Menu()
    menuBar.Append(menu, menuData.name)
    appendItems(window, menu, menuData)


def createMenuBar(window, menuData):
    """Creates a menu bar in the given window.
    menuData is a composition of the classes above.
    """
    menuBar = wx.MenuBar()
    for menu in menuData:
        createMenu(window, menuBar, menu)
    window.SetMenuBar(menuBar)


def getMenuItem(self, event):
    """Returns the menu item that triggered an EVT_MENU.
    Can be used to manipulate the correspondending item
    (e.g. change label text, disable ...)
    """
    return self.GetMenuBar().FindItemById(event.GetId())


def findMenuInMenuBar(menuBar, title):
    """Search for a menu entry in top-level menu.
    """
    pos = menuBar.FindMenu(title)
    if pos == wx.NOT_FOUND:
        return None
    return menuBar.GetMenu(pos)

"""
 Occasionally, you will have multiple menu items that need to be bound to the
same handler. For example, a set of radio button toggle menus, all of which do
essentially the same thing, may be bound to the same handler. To avoid having to
bind each one separately, if the menu items have consecutive identifier numbers,
use the  wx.EVT_MENU_RANGE  event type:

self.Bind(wx.EVT_MENU_RANGE, function, id=menu1, id2=menu2)
"""

