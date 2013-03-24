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


myEVT_BUTTON_CHANGED = wx.NewEventType()
EVT_BUTTON_CHANGED = wx.PyEventBinder(myEVT_BUTTON_CHANGED, 1)


class ButtonChangedEvent(wx.PyCommandEvent):
    def __init__(self, evtType, _id):
        super(ButtonChangedEvent, self).__init__(evtType, _id)
        self._state = None

    def setState(self, val):
        self._state = val

    def getState(self):
        return self._state



class MultipleChoiceButtons(wx.Panel):
    def __init__(self, parent, buttons, label = '', horizontal = True, default = None):
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)

        staticBox = wx.StaticBox(self, label = ' %s ' % label.strip())
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)

        sizer = wx.BoxSizer(wx.HORIZONTAL if horizontal else wx.VERTICAL)

        self.buttonDict = dict()

        for buttonName in buttons:
            btn = wx.ToggleButton(self, label = buttonName, id =  wx.NewId())
            btn.Bind(wx.EVT_TOGGLEBUTTON, self.buttonClicked)
            sizer.Add(btn, 1, wx.ALL | wx.ALIGN_BOTTOM, 5)
            self.buttonDict[buttonName] = btn

        if not default:
            default = buttons[0]
        self._activeButton = self.buttonDict[default]
        self._activeButton.SetValue(True)

        staticBoxSizer.Add(sizer)
        self.SetSizerAndFit(staticBoxSizer)

    def buttonClicked(self, event):
        button = event.GetEventObject()

        self.setActiveButton(button)
        evt = ButtonChangedEvent(myEVT_BUTTON_CHANGED, self.GetId())
        evt.setState(button.GetLabel())
        self.GetEventHandler().ProcessEvent(evt)

    def getActiveButtonName(self):
        return self._activeButton.GetLabel()

    def setActiveButtonByName(self, name):
        self.setActiveButton(self.buttonDict[name])

    def setActiveButton(self, button):
        if button == self._activeButton:
            button.SetValue(True)
        else:
            self._activeButton.SetValue(False)
            self._activeButton = button
            button.SetValue(True)


class ToggleButton(wx.ToggleButton):
    """Extends wx.ToggleButton with active/inactive labels.
    """
    def __init__(self, parent, labelOn, labelOff, bgColorOn = wx.Color(0, 255, 0)):
        wx.ToggleButton.__init__(self, parent = parent, label = labelOn, id = wx.ID_ANY)
        self.labelOn = labelOn
        self.labelOff = labelOff
        self.bgColorOff = self.GetBackgroundColour()
        self.bgColorOn = bgColorOn

        self.Bind(wx.EVT_TOGGLEBUTTON, self.buttonToggled)

    def setState(self, state):
        self.SetValue(state)
        self._setStateInternal(state)

    def getState(self):
        return self.GetValue()

    def _setStateInternal(self, state):
        if state == True:       # Active State.
            self.SetLabel(self.labelOff)
            self.SetBackgroundColour(self.bgColorOn)
        elif state == False:    # Inactive State.
            self.SetLabel(self.labelOn)
            self.SetBackgroundColour(self.bgColorOff)


    def buttonToggled(self, event):
        state = event.EventObject.GetValue()

        self._setStateInternal(state)
        evt = ButtonChangedEvent(myEVT_BUTTON_CHANGED, self.GetId())
        evt.setState(state)
        self.GetEventHandler().ProcessEvent(evt)

ToggleButton.EVT_BUTTON_CHANGED = EVT_BUTTON_CHANGED
MultipleChoiceButtons.EVT_BUTTON_CHANGED = EVT_BUTTON_CHANGED

