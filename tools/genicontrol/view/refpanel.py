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
#import math
#import genicontrol.conversion as conversion

import wx
import math
import threading
import genicontrol.apdu as apdu
import genicontrol.defs as defs
#import genicontrol.model.ModelIf as ModelIf
from wx.lib.scrolledpanel import ScrolledPanel
import genicontrol.dataitems as dataitems
from genicontrol.model.config import DataitemConfiguration, REFERENCES_DICT
import genicontrol.controlids as controlids
from decimal import Decimal as D
from genicontrol.scaling import getScalingInfo
from genilib.utils import dumpHex, makeWord

CONTROL_MODE_AUTOADAPT              = 0
CONTROL_MODE_CONSTANT_PRESSURE      = 1
CONTROL_MODE_PROPORTIONAL_PRESSURE  = 2
CONTROL_MODE_CONSTANT_FREQUENCY     = 3

# Control mode names (as reported by the pump, see dissect.py) and the commands to select them.
CONTROL_MODE_BY_NAME = {
    'AutoAdapt':                CONTROL_MODE_AUTOADAPT,
    'Constant Pressure':        CONTROL_MODE_CONSTANT_PRESSURE,
    'Proportional Pressure':    CONTROL_MODE_PROPORTIONAL_PRESSURE,
    'Constant Frequency':       CONTROL_MODE_CONSTANT_FREQUENCY,
}
CONTROL_MODE_COMMAND = {
    CONTROL_MODE_AUTOADAPT:             'AutoAdapt',
    CONTROL_MODE_CONSTANT_PRESSURE:     'CONST_PRESS',
    CONTROL_MODE_PROPORTIONAL_PRESSURE: 'PROP_PRESS',
    CONTROL_MODE_CONSTANT_FREQUENCY:    'CONST_FREQ',
}

HEIGHT_CHOICES = ['%.1f' % (x / 2.0) for x in range(2, 13)]     # 1.0 .. 6.0 m
PERCENT_CHOICES = ['%d' % x for x in range(0, 101, 10)]         # 0 .. 100 %

CONTROL_MODE_MAP = {
    CONTROL_MODE_AUTOADAPT:             controlids.ID_CMD_AUTOADAPT,
    CONTROL_MODE_CONSTANT_PRESSURE:     controlids.ID_CMD_CONST_PRESS,
    CONTROL_MODE_PROPORTIONAL_PRESSURE: controlids.ID_CMD_PROP_PRESS,
    CONTROL_MODE_CONSTANT_FREQUENCY:    controlids.ID_CMD_CONST_FREQ
}

class RefPanel(ScrolledPanel):
    def __init__(self, parent):
        self._concurrentAccess = threading.Lock()
        self._refsetRequested = False
        self._connected = False
        self._raw = {}      # Raw values (0..254) as read from the pump.
        self._pumpControlMode = None    # Control mode name as reported by the pump.
        self._sourceMode = None         # 'Remote' / 'Local' as reported by the pump.
        #self._model = model

        ScrolledPanel.__init__(self, parent = parent, id = wx.ID_ANY)

        sizer = self.addValues()

        self.btnSetRefValues = wx.Button(self, label = "Set Reference Value", id = controlids.ID_SET_REFERENCE_VALUES)
        sizer.Add(self.btnSetRefValues, (len(DataitemConfiguration['ReferenceValues']), 0), wx.DefaultSpan, wx.ALL | wx.ALIGN_LEFT, 5)
        self.btnSetRefValues.Bind(wx.EVT_BUTTON, self.onRefSet)

        height = HEIGHT_CHOICES
        self.cb = wx.ComboBox(self, choices=height, style=wx.CB_READONLY)
        self.cb.SetValue('3.0')
        sizer.Add(self.cb, (len(DataitemConfiguration['ReferenceValues']), 1), wx.DefaultSpan, wx.ALL | wx.ALIGN_RIGHT, 5)
        self.cb.Bind(wx.EVT_COMBOBOX, self.onSelect)
        ctrl = wx.StaticText(self, wx.ID_ANY, "m", style = wx.ALIGN_RIGHT)
        self.cbUnit = ctrl
        sizer.Add(ctrl, (len(DataitemConfiguration['ReferenceValues']), 2), wx.DefaultSpan, wx.ALL | wx.ALIGN_LEFT, 5)

        static_box = wx.StaticBox(self, label = 'Control-Mode')
        groupSizer = wx.StaticBoxSizer(static_box, wx.HORIZONTAL)
        btnConstPressure = wx.ToggleButton(self, label = 'Constant Pressure', id = controlids.ID_CMD_CONST_PRESS)
        groupSizer.Add(btnConstPressure, 1, wx.ALL, 5)
        btnPropPressure = wx.ToggleButton(self, label = 'Proportional Pressure', id = controlids.ID_CMD_PROP_PRESS)
        groupSizer.Add(btnPropPressure, 1, wx.ALL, 5)
        btnConstFreq = wx.ToggleButton(self, label = 'Constant Frequency', id = controlids.ID_CMD_CONST_FREQ)
        groupSizer.Add(btnConstFreq, 1, wx.ALL, 5)
        btnAutoAdapt = wx.ToggleButton(self, label = 'AutoAdapt', id = controlids.ID_CMD_AUTOADAPT)
        self.btnBgColor = btnAutoAdapt.GetBackgroundColour()
        groupSizer.Add(btnAutoAdapt, 1, wx.ALL, 5)
        self.setControlMode(CONTROL_MODE_CONSTANT_PRESSURE)

        btnConstPressure.controlMode = CONTROL_MODE_CONSTANT_PRESSURE
        btnPropPressure.controlMode = CONTROL_MODE_PROPORTIONAL_PRESSURE
        btnConstFreq.controlMode = CONTROL_MODE_CONSTANT_FREQUENCY
        btnAutoAdapt.controlMode = CONTROL_MODE_AUTOADAPT

        self.Bind(wx.EVT_TOGGLEBUTTON, self.choiceButton, btnConstPressure)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.choiceButton, btnPropPressure)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.choiceButton, btnConstFreq)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.choiceButton, btnAutoAdapt)

        sizer.Add(groupSizer, ((len(DataitemConfiguration['ReferenceValues']) + 1), 0), (1, 3), wx.ALL | wx.GROW, 5)

        self.SetSizerAndFit(sizer)
        self.SetupScrolling()

        self.itemDict = dict([(x[0], x[1:]) for x in DataitemConfiguration['ReferenceValues']])

    def choiceButton(self, event):
        """Control mode button clicked: send the command to the pump."""
        mode = event.EventObject.controlMode
        model = getattr(self, '_model', None)
        previous = getattr(self, '_mode', None)
        if model is None or not getattr(model, 'online', False) or mode == previous:
            self.setControlMode(previous if previous is not None else mode)   # Undo the toggle.
            return
        switchToRemote = False
        if self._sourceMode != 'Remote':
            # Control mode commands from the bus are accepted in LOCAL mode, but only take
            # effect in REMOTE mode -- the pump would just keep its local control mode.
            if not self.askSwitchToRemote():
                self.setControlMode(previous if previous is not None else mode)   # Undo the toggle.
                return
            switchToRemote = True
        self.setControlMode(mode)   # Optimistic; corrected by the next status update from the pump.
        if switchToRemote:
            model.switchToRemote(self._raw.get('ref_rem'))
        model.sendCommand(CONTROL_MODE_COMMAND[mode], refreshReferences = True)

    def askSwitchToRemote(self):
        dlg = wx.MessageDialog(self,
            "The pump is in LOCAL mode.\n\n"
            "A control mode sent via GENIbus only takes effect in REMOTE mode.\n"
            "Switch the pump to REMOTE now?\n\n"
            "Note: in REMOTE mode the pump uses the bus setpoint (Remote reference)\n"
            "instead of the setpoint adjusted at the pump.",
            "GeniControl - Control mode", wx.YES_NO | wx.ICON_QUESTION)
        try:
            return dlg.ShowModal() == wx.ID_YES
        finally:
            dlg.Destroy()

    def setPumpStatus(self, item, value):
        """Status information from the pump (see dissect.dissectPumpStatus)."""
        if item == 'controlMode':
            self._pumpControlMode = value
            mode = CONTROL_MODE_BY_NAME.get(value)
            if mode is not None and mode != getattr(self, '_mode', None):
                self.setControlMode(mode)
            self.updateSetpointChoices()
            self.updateDisplay()
        elif item == 'sourceMode':
            self._sourceMode = value
            self.updateDisplay()

    def isFrequencyMode(self):
        return self._pumpControlMode == 'Constant Frequency'

    def isAutoAdapt(self):
        # AutoAdapt: the pump determines the setpoint itself, ref_rem / ref_ir are not used.
        return self._pumpControlMode == 'AutoAdapt'

    def updateSetpointChoices(self):
        choices, unit = (PERCENT_CHOICES, "%") if self.isFrequencyMode() else (HEIGHT_CHOICES, "m")
        if self.cbUnit.GetLabel() != unit:
            self.cb.Set(choices)
            self.cb.SetValue(choices[len(choices) // 2])
            self.cbUnit.SetLabel(unit)
        enable = not self.isAutoAdapt()
        self.cb.Enable(enable)
        self.btnSetRefValues.Enable(enable)
        self.btnSetRefValues.SetToolTip("" if enable else "AutoAdapt: the pump determines the setpoint itself.")

    def addValues(self):

        sizer = wx.GridBagSizer(hgap=5, vgap=5)

        for idx, item in enumerate(DataitemConfiguration['ReferenceValues']):
            key, displayName, unit, controlIdValue, controlIdUnit = item

            if key in ('ref_rem', 'ref_ir'):
                ditem = dataitems.REFERENCES[key]
            else:
                ditem = dataitems.MEASUREMENT_VALUES[key]

            ctrl = wx.StaticText(self, wx.ID_ANY, displayName, style = wx.ALIGN_RIGHT)
            ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 0), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.TextCtrl(self, controlIdValue, "n/a", style = wx.ALIGN_RIGHT)
            ctrl.SetEditable(False)    # read-only, but not greyed out
            ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 1), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.StaticText(self, controlIdUnit, unit, style = wx.ALIGN_LEFT)
            sizer.Add(ctrl, (idx, 2), wx.DefaultSpan, wx.ALL | wx.ALIGN_LEFT, 5)

        return sizer

    def getButtonForMode(self, mode):
        controlID = CONTROL_MODE_MAP[mode]
        control = self.FindWindowById(controlID)
        return control

    def setControlMode(self, mode):
        if hasattr(self, '_mode'):
            control = self.getButtonForMode(self._mode)
            control.SetValue(False)
            control.SetBackgroundColour(self.btnBgColor)
        self._mode = mode
        control = self.getButtonForMode(mode)
        control.SetValue(True)
        control.SetBackgroundColour(wx.Colour(0, 255, 0))

    def getControlMode(self):
        return self._mode

    # Values relative to the r_min..r_max subinterval / relative to the sys_fb range.
    RELATIVE_TO_SUBINTERVAL = ('ref_rem', 'ref_ir', 'ref_act')
    RELATIVE_TO_FEEDBACK = ('sys_fb', 'r_min', 'r_max')

    def setValue(self, item, value):
        if item in REFERENCES_DICT:
            self._raw[item] = value
            self.updateDisplay()

    def toMeters(self, item, raw):
        """Convert a raw reference value (0..254) to head in m (None, if not possible yet)."""
        try:
            raw = int(raw)
            if raw > 254:
                return None     # 0xff: not available.
            if self.isFrequencyMode() and item != 'sys_fb':
                return None     # Constant frequency: setpoints are speeds (%), not heads.
            fbMin, fbMax = [float(x) for x in self.getFeedbackRange()]
            if item in self.RELATIVE_TO_FEEDBACK:
                scaled = raw
            else:
                rMin, rMax = int(self._raw['r_min']), int(self._raw['r_max'])
                scaled = rMin + raw * (rMax - rMin) / 254.0
            return fbMin + scaled * (fbMax - fbMin) / 254.0
        except (KeyError, TypeError, ValueError):
            return None

    def updateDisplay(self):
        for item, raw in self._raw.items():
            _, _, controlID, controlIdUnit = REFERENCES_DICT[item]
            control = self.FindWindowById(controlID)
            unitCtrl = self.FindWindowById(controlIdUnit)
            meters = self.toMeters(item, raw)
            try:
                percent = int(raw) * 100.0 / 254.0     # GENIbus: 254 = 100 %
                base = "of r_min..r_max" if item in self.RELATIVE_TO_SUBINTERVAL else "of sensor range"
                percentText = "%.1f %% %s" % (percent, base) if int(raw) <= 254 else "n/a"
            except (TypeError, ValueError):
                percentText = "n/a"
            if meters is None:
                text = percentText.split(' %')[0]
                unit = ("%%   (%s)" % percentText.split('% ')[1]) if ' of ' in percentText else ""
            else:
                text, unit = "%.2f" % meters, "m   (%s)" % percentText
            if self.isAutoAdapt() and item in ('ref_rem', 'ref_ir'):
                text, unit = "-", "     (not used in AutoAdapt)"
            if control:
                control.SetToolTip("raw value: %s" % raw)
            if control:
                control.SetValue(text)
            if unitCtrl:
                unitCtrl.SetLabel(unit)
        self.Layout()
        self.updatePumpOperation()

    def physicalValue(self, item):
        """(text, unit) of a reference value for display: m, or % in constant frequency mode."""
        raw = self._raw.get(item)
        if raw is None:
            return 'n/a', ''
        meters = self.toMeters(item, raw)
        if meters is not None:
            return "%.2f" % meters, 'm'
        try:
            if int(raw) <= 254:
                return "%.1f" % (int(raw) * 100.0 / 254.0), '%'
        except (TypeError, ValueError):
            pass
        return 'n/a', ''

    def updatePumpOperation(self):
        """Fill 'Setpoint' / 'Actual Setpoint' on the 'Measurement + Control' page."""
        try:
            panel = self.GetParent().mcPanel.pumpOperationPanel
        except AttributeError:
            return
        # The setpoint in use depends on the control source: bus (remote) or pump/GENIlink (local).
        setpointItem = 'ref_rem' if self._sourceMode == 'Remote' else 'ref_ir'
        for name, item in (("Setpoint", setpointItem), ("Actual Setpoint", 'ref_act')):
            text, unit = self.physicalValue(item)
            if name == "Setpoint" and self.isAutoAdapt():
                text, unit = "auto", ""
            panel.setValue(name, text)
            panel.setUnit(name, unit)

    def onSelect(self, event):
        cb_item = event.GetSelection()
        height = self.cb.GetValue()
        #print("cb_item:", cb_item, height)

    def writeToServer(self, req):
        self._model.writeToServer(req)
        #self._connection.write(req)
        #self._controller.trace(False, req)

    def calculateSetpoint(self, x, sys_fb_min, sys_fb_max, r_min, r_max):
#ref_rem = ((height-sys_fb_min)/(sys_fb_max - sys_fb_min)*254 - r_min)*254/(r_max-r_min)
        return ((D(x) - D(sys_fb_min)) / (D(sys_fb_max) - D(sys_fb_min)) * D('254.0') - D(r_min)) * D('254.0') / (D(r_max) - D(r_min))

    def setRefValue(self):
        x = self.cb.GetValue()
        if self.isFrequencyMode():
            # Constant frequency: setpoint in % of the r_min..r_max interval.
            value = D(x) * D('254') / D('100')
            print("Setpoint %s %% -> ref_rem=%.1f" % (x, value))
            return value
        r_min = str(self._raw['r_min'])
        r_max = str(self._raw['r_max'])
        sys_fb_min, sys_fb_max = self.getFeedbackRange()
        value = self.calculateSetpoint(x, sys_fb_min, sys_fb_max, r_min, r_max)
        print("Setpoint %s m: sys_fb range %s..%s m, r_min=%s, r_max=%s -> ref_rem=%.1f" % (
            x, sys_fb_min, sys_fb_max, r_min, r_max, value))
        return value

    def getFeedbackRange(self):
        """Physical range of 'sys_fb' (system feedback, head in m), from the pump's INFO data."""
        model = getattr(self, '_model', None)
        try:
            info = model.getInfo(defs.APDUClass.MEASURED_DATA, 'sys_fb')
            factor = D(str(getScalingInfo(info).factor))
            return str(D(info.zero) * factor), str((D(info.zero) + D(info.range)) * factor)
        except Exception:
            return '0', '20'     # Fallback (old default).

    def onRefSet(self, event):
        model = getattr(self, '_model', None)
        if model is None:
            return
        try:
            value = int(float(self.setRefValue()) + 0.5)    # round, not truncate (3.0 m -> 112, not 111)
        except Exception as e:
            wx.MessageBox("Cannot calculate reference value (are r_min / r_max available?):\n%s" % e,
                "GeniControl", wx.OK | wx.ICON_WARNING, self)
            return
        value = max(0, min(value, 254))
        self._refsetRequested = True
        model.setReferenceValue('ref_rem', value)

#    uint8 ref_rem_set[13] = {0x27,0x09,0x20,0x01,0x03,0x81,0x07,0x05,0x82,0x01,0x53,0x00,0x00};
#    uint8 ref_ir_set[13]  = {0x27,0x06,0x20,0x01,0x05,0x82,0x02,0x53,0x00,0x00}; //2,5m
#    uint8 ref_ir_set[13]  = {0x27,0x06,0x20,0x01,0x05,0x82,0x02,0x70,0x00,0x00}; //3,0m

"""
    def toggledbutton(self, event):
        # Active State
        if event.EventObject.GetValue() == True:
            event.EventObject.SetLabel(event.EventObject.labelOff)
            event.EventObject.SetBackgroundColour(wx.Colour(0, 255, 0))
        # Inactive State
        if event.EventObject.GetValue() == False:
            event.EventObject.SetLabel(event.EventObject.labelOn)
            event.EventObject.SetBackgroundColour(event.EventObject.bgColor)
"""
