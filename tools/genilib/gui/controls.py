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

def createLabeledControl(parent, label, control, sizer, group = None):
    """Create a control with a label, i.e. wx.StaticText to the left.

    parent - window which control belongs to.
    label - descriptive text.
    control - arbitrary control.
    sizer - sizer which control will be added to.
    group - a list collecting related controls, very useful to disable/enable a group of controls
    """
    st = wx.StaticText(parent, label = label)
    sizer.Add(st, 1, wx.ALL | wx.ALIGN_LEFT, 5)
    if group is not None:
        group.append(control)
    sizer.Add(control, 1, wx.ALL | wx.ALIGN_RIGHT, 5)
    return control

