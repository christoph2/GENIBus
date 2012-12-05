#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
import locale
import wx

import genicontrol.dataitems as dataitems
import genicontrol.view
import genicontrol.model.NullModel as NullModel
import genicontrol.observer as observer

try:
    import ConfigParser as configparser
except ImportError:
    import configparser # Python 3.x

TR = wx.GetTranslation

ID_CMD_REMOTE_LOCAL         = wx.NewId()

ID_CMD_START_STOP           = wx.NewId()

ID_CMD_MIN                  = wx.NewId()
ID_CMD_MAX                  = wx.NewId()

ID_CMD_RUN                  = wx.NewId()
ID_CMD_PROGRAM              = wx.NewId()
ID_CMD_CONST_FREQ           = wx.NewId()
ID_CMD_CONST_PRESS          = wx.NewId()
ID_CMD_PROP_PRESS           = wx.NewId()
ID_CMD_REF_UP               = wx.NewId()
ID_CMD_REF_DOWN             = wx.NewId()
ID_CMD_AUTOMATIC            = wx.NewId()
ID_CMD_NIGHT_REDUCE_E       = wx.NewId()
ID_CMD_NIGHT_REDUCE_D       = wx.NewId()
ID_CMD_LOCK_KEYS            = wx.NewId()
ID_CMD_UNLOAD_KEYS          = wx.NewId()

ID_MEAS_SPEED               = wx.NewId()
ID_MEAS_HEAD                = wx.NewId()
ID_MEAS_FLOW                = wx.NewId()
ID_MEAS_POWER               = wx.NewId()
ID_MEAS_ENERGY              = wx.NewId()
ID_MEAS_HOURS               = wx.NewId()

ID_REF_REM                  = wx.NewId()
ID_REF_IR                   = wx.NewId()
ID_REF_ATT_REM              = wx.NewId()

ID_PARAM_UNIT_ADDR          = wx.NewId()
ID_PARAM_GROUP_ADDR         = wx.NewId()
ID_PARAM_H_CONST_REF_MIN    = wx.NewId()
ID_PARAM_H_CONST_REF_MAX    = wx.NewId()
ID_PARAM_H_PROP_REF_MIN     = wx.NewId()
ID_PARAM_H_PROP_REF_MIN     = wx.NewId()
ID_PARAM_H_PROP_REF_MAX     = wx.NewId()
ID_PARAM_REF_STEPS          = wx.NewId()

ID_STR_PRODUCT_NAME         = wx.NewId()
ID_STR_SOFTWARE_NAME1       = wx.NewId()
ID_STR_COMPILE_DATE1        = wx.NewId()
ID_STR_PROTOCOL_CODE        = wx.NewId()
ID_STR_DEVELOPERS           = wx.NewId()
ID_STR_RTOS_CODE            = wx.NewId()

##
##
ID_SET_REFERENCE_VALUES     = wx.NewId()


CONTROL_MODE_AUTOMATIC              = 0
CONTROL_MODE_CONSTANT_PRESSURE      = 1
CONTROL_MODE_PROPORTIONAL_PRESSURE  = 2
CONTROL_MODE_CONSTANT_FREQUENCY     = 3

import led

class TabPanel(wx.Panel):
    def __init__(self, parent):
        """"""

        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        sizer = wx.BoxSizer(wx.VERTICAL)
        txtOne = wx.TextCtrl(self, wx.ID_ANY, "")
        txtTwo = wx.TextCtrl(self, wx.ID_ANY, "")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(txtOne, 0, wx.ALL, 5)
        sizer.Add(txtTwo, 0, wx.ALL, 5)

        self.SetSizer(sizer)


"""
    f_act -performance in % (here shown as a bar graph).
"""

MY_MEAS_VALUES = (
    ('speed',       u'Speed',       u'rpm'),
    ('h',           u'Head',        u'm'),
    ('q',           u'Flowrate',    u'm³/h'),
    ('p',           u'Power' ,      u'W'),
    ('energy_hi',   u'Energy',      u'kWh'),
    ('t_2hour_hi',  u'Hours',       u'h'),
)

MY_REF_VALUES = (
    ("ref_rem",     u'GENIBus ref.',    u'%'),
    ('ref_ir',      u'GENIlink ref.',   u''),
    ('ref_att_rem', u'Ext. Analogue',   u'%'),
)

MY_STRING_VALUES = (
    ("product_name",    "Product name"      , ID_STR_PRODUCT_NAME),
    ("software_name1",  "Software name"     , ID_STR_SOFTWARE_NAME1),
    ("compile_date1",   "Compilation date"  , ID_STR_COMPILE_DATE1),
    ("protocol_code",   "Protocol code"     , ID_STR_PROTOCOL_CODE),
    ("developers",      "Developers"        , ID_STR_DEVELOPERS),
    ("rtos_code",       "RTOS code"         , ID_STR_RTOS_CODE),
)

MY_INFO_VALUES = (
    "t_2hour_hi",
    "i_dc",
    "v_dc",
    "t_e",
    "t_m",
    "i_mo",
    "i_line",
    "f_act",
    "p",
    "speed",
    "h",
    "q",
    "ref_loc",
    "p_max",
    "q_kn1",
    "q_max",
    "h_max",
    "ind_alarm_bak",
    "led_contr",
    "ref_act",
    "ref_inf",
    "t_w",
    "ref_att_loc",
    "sys_ref",
    "start_alarm1",
    "start_alarm2",
    "qsd_alarm1",
    "qsd_alarm2",
    "stop_alarm1",
    "stop_alarm2",
    "surv_alarm1",
    "surv_alarm2",
    "ind_alarm",
    "start_alarm1_bak",
    "start_alarm2_bak",
    "qsd_alarm1_bak",
    "qsd_alarm2_bak",
    "stop_alarm1_bak",
    "stop_alarm2_bak",
    "surv_alarm1_bak",
    "surv_alarm2_bak",
    "act_mode1",
    "act_mode2",
    "act_mode3",
    "loc_setup1",
    "rem_setup1",
    "extern_inputs",
    "contr_source",
    "stop_alarm3",
    "stop_alarm3_bak",
    "curve_no_ref",
    "contr_ref",
    "unit_family",
    "unit_type",
    "unit_version",
    "energy_hi",
    "alarm_code_disp",
    "alarm_code",
    "alarm_log_1",
    "alarm_log_2",
    "alarm_log_3",
    "alarm_log_4",
    "alarm_log_5",
    "twin_pump_mode",
)


class StatusPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)
        sizer = self.addValues()
        ctrl = wx.StaticText(self, wx.ID_ANY, 'Performance', style = wx.ALIGN_RIGHT)
        sizer.Add(ctrl, (6, 0), wx.DefaultSpan, wx.ALL, 5)

        gauge = wx.Gauge(parent = self, range = 100)
        gauge.SetToolTip(wx.ToolTip('n/a'))
        gauge.SetValue(0)
        sizer.Add(gauge, (6, 1), (1, 1), wx.ALL, 5)

        ctrl = wx.StaticText(self, wx.ID_ANY, '%', style = wx.ALIGN_RIGHT)
        sizer.Add(ctrl, (6, 2), wx.DefaultSpan, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.SetSizer(sizer)

    def addValues(self):
        #sizer = wx.GridSizer(len(MY_MEAS_VALUES), 3, 0, 0)
        sizer = wx.GridBagSizer(5, 45)
        for idx, item in enumerate(MY_MEAS_VALUES):
            key, displayName, unit = item
            ditem =  dataitems.MEASUREMENT_VALUES[key]

            ctrl = wx.StaticText(self, wx.ID_ANY, displayName, style = wx.ALIGN_RIGHT)
            ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 0), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.TextCtrl(self, wx.ID_ANY, "n/a", style = wx.ALIGN_RIGHT)
            ctrl.Enable(False)
            ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 1), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.StaticText(self, wx.ID_ANY, unit, style = wx.ALIGN_RIGHT)
            sizer.Add(ctrl, (idx, 2), wx.DefaultSpan, wx.ALL | wx.ALIGN_RIGHT, 5)
        return sizer

ToggleButton = namedtuple('ToggleButton', 'id, labelOn, labelOff attrName')

def createToggleButton(parent, buttonDesc, sizer):
    btn = wx.ToggleButton(parent, label = buttonDesc.labelOn, id = buttonDesc.id)
    sizer.Add(btn, 1, wx.ALL, 5)
    setattr(parent, buttonDesc.attrName, btn)
    return btn

class Controls(wx.Panel):
    def __init__(self, parent):
        self.toggleButtons = (
            ToggleButton(ID_CMD_REMOTE_LOCAL, 'Remote', 'Local', 'btnRemoteLocal'),
            ToggleButton(ID_CMD_START_STOP, 'Start', 'Stop', 'btnStartStop'),
            # ToggleButton(ID_CMD_MIN_MAX, 'Min', 'Max'),
        )
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)
        #self.btn = wx.ToggleButton(self, label = 'Fork me!', id = wx.ID_ANY)
        #self.btn.SetBackgroundColour(wx.Colour(255,0,0))
        #self.Bind(wx.EVT_TOGGLEBUTTON, self.toggledbutton, self.btn)
        sizer1 = wx.BoxSizer(wx.VERTICAL)

        sizer3 = wx.BoxSizer(wx.HORIZONTAL)

        sizer3.Add(wx.StaticText(self, -1, ''), 1, wx.ALL, 5)
        self.btnRefUp = wx.Button(self, label = '+', id = ID_CMD_REF_UP)
        sizer3.Add(self.btnRefUp, 1, wx.ALL | wx.GROW, 5)
        self.btnRefDown = wx.Button(self, label = '-', id = ID_CMD_REF_DOWN)
        sizer3.Add(self.btnRefDown, 1, wx.ALL | wx.GROW, 5)
        sizer1.Add(sizer3)#, 1, wx.ALL, 5)

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        for btn in self.toggleButtons:
            createToggleButton(self, btn, sizer2)

        btn = wx.Button(self, label = 'Min', id = ID_CMD_MIN)
        sizer2.Add(btn, 1, wx.ALL, 5)
        btn = wx.Button(self, label = 'Max', id = ID_CMD_MAX)
        sizer2.Add(btn, 1, wx.ALL, 5)

        sizer1.Add(sizer2) # , 1, wx.ALL, 5)
        self.SetSizer(sizer1)

        self.enableControls((ID_CMD_MAX, ID_CMD_MIN))

    def toggledbutton(self, event):
        # Active State
        if self.btn.GetValue() == True:
            self.btn.SetLabel('Stop')
            self.btn.SetBackgroundColour(wx.Color(0, 255, 0))
        # Inactive State
        if self.btn.GetValue() == False:
            self.btn.SetLabel('Start')
            self.btn.SetBackgroundColour(wx.Color(255, 0, 0))

    def setRemoteMode(self):
        pass

    def setLocalMode(self):
        pass

    def setStartMode(self):
        pass

    def setStopMode(self):
        pass

    def enableControls(self, controlIDs):
        for controlID in controlIDs:
            control = self.FindWindowById(controlID)
            control.Enable(True)

    def disableControls(self, controlIDs):
        for controlID in controlIDs:
            control = self.FindWindowById(controlID)
            control.Enable(False)

class MCPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)

        #wx.StaticBox(self, wx.ID_ANY, 'Pump status')
        sizer = wx.BoxSizer(wx.VERTICAL)

        statusPanel = StatusPanel(self)
        #statusPanel.SetMinSize(statusPanel.GetSize())
        sizer.Add(statusPanel) # , wx.GROW | wx.ALL, 5)
        controlsPanel = Controls(self)
        sizer.Add(controlsPanel) #, 1, wx.ALL | wx.GROW, 5)
        #st = wx.StaticText(self, wx.ID_ANY, '')
        #st.SetForegroundColour(wx.Color(0, 0, 255))
        #sizer.Add(st, 1, wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Layout()
        sizer.Fit(self)

class RefPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)

        sizer = self.addValues()
        self.btnSetRefValues = wx.Button(self, label = "Set Reference Values", id = ID_SET_REFERENCE_VALUES)

        static_box = wx.StaticBox(self, label = 'Control-Mode')
        groupSizer = wx.StaticBoxSizer(static_box, wx.HORIZONTAL)
        btnConstPressure = wx.ToggleButton(self, label = 'Constant Pressure', id = ID_CMD_CONST_PRESS)
        groupSizer.Add(btnConstPressure, 1, wx.ALL, 5)
        btnPropPressure = wx.ToggleButton(self, label = 'Proportional Pressure', id = ID_CMD_PROP_PRESS)
        groupSizer.Add(btnPropPressure, 1, wx.ALL, 5)
        btnConstFreq = wx.ToggleButton(self, label = 'Constant Frequency', id = ID_CMD_CONST_FREQ)
        groupSizer.Add(btnConstFreq, 1, wx.ALL, 5)
        btnAutomatic = wx.ToggleButton(self, label = 'Automatic', id = ID_CMD_AUTOMATIC)
        groupSizer.Add(btnAutomatic, 1, wx.ALL, 5)

        #sl = wx.StaticLine(self)
        #groupSizer.Add(sl)

        sizer.Add(groupSizer, (len(MY_REF_VALUES), 0), (1, 3), wx.ALL | wx.GROW, 5)

        sizer.Add(self.btnSetRefValues, ((len(MY_REF_VALUES) + 1), 0), wx.DefaultSpan, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.SetSizer(sizer)

    def addValues(self):
        sizer = wx.GridBagSizer(5, 45)
        for idx, item in enumerate(MY_REF_VALUES):
            key, displayName, unit = item
            ditem =  dataitems.REFERENCES[key]

            ctrl = wx.StaticText(self, wx.ID_ANY, displayName, style = wx.ALIGN_RIGHT)
            ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 0), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.TextCtrl(self, wx.ID_ANY, "n/a", style = wx.ALIGN_RIGHT)
            ctrl.Enable(False)
            ctrl.SetToolTip(wx.ToolTip(ditem.note))
            sizer.Add(ctrl, (idx, 1), wx.DefaultSpan, wx.ALL, 5)

            ctrl = wx.StaticText(self, wx.ID_ANY, unit, style = wx.ALIGN_LEFT)
            sizer.Add(ctrl, (idx, 2), wx.DefaultSpan, wx.ALL | wx.ALIGN_RIGHT, 5)
        return sizer


    def setControlMode(self, mode, unset = False):
        if mode == CONTROL_MODE_AUTOMATIC:
            controlID = ID_CMD_AUTOMATIC
        elif mode == CONTROL_MODE_CONSTANT_PRESSURE:
            controlID = ID_CMD_CONST_PRESS
        elif mode == CONTROL_MODE_PROPORTIONAL_PRESSURE:
            controlID = ID_CMD_PROP_PRESS
        elif mode == CONTROL_MODE_CONSTANT_FREQUENCY:
            controlID = ID_CMD_CONST_FREQ
        control = self.FindWindowById(controlID)

from view.GridControl import GridControl

class InfoPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent = parent, id = wx.ID_ANY)
        sizer = self.addValues(MY_STRING_VALUES)
        grid = GridControl(self, MY_INFO_VALUES, dataitems.DATAITEMS)
        sizer.Add(grid, 1, wx.ALL, 5)
        self.SetSizer(sizer)

    def addValues(self, values):
        sizer = wx.BoxSizer(wx.VERTICAL)
        for datapoint, displayName,idCode in values:
            hsizer = wx.BoxSizer(wx.HORIZONTAL)
            st = wx.StaticText(self, label = displayName)
            hsizer.Add(st, 1, wx.ALL, 5)
            tc = wx.TextCtrl(self, idCode, "n/a", style = wx.ALIGN_RIGHT)
            tc.Enable(False)
            hsizer.Add(tc, 1, wx.ALL, 5)
            sizer.Add(hsizer) # , 1, wx.ALL, 5)
        return sizer

    def setValue(self, controlID, value):
        control = self.GetWindowById(controlID)
        control.SetValue(value)

class TestNB(wx.Notebook):
    def __init__(self, parent, id):
        wx.Notebook.__init__(self, parent, id, size=(21,21), style=
                             wx.BK_DEFAULT | wx.BK_BOTTOM
                             #wx.BK_TOP
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )
        tabOne = TabPanel(self)
        #tabOne.SetBackgroundColour("Gray")
        self.AddPage(MCPanel(self), "Measurement + Control")
        self.AddPage(tabOne, "Busmonitor")
        self.AddPage(RefPanel(self), "References")
        self.AddPage(tabOne, "Parameters")
        self.AddPage(InfoPanel(self), "Info")


class GBFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "GeniControl", size=(800,600))
        self.initStatusBar()
        self.createMenuBar()

        self.locale = None
        self.updateLanguage(wx.LANGUAGE_ITALIAN)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

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
        wx.LogMessage("Started...")

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
                    ("&Exit", "Exit GeniControl", self.OnCloseWindow)))

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

    def OnCloseWindow(self, event):
        wx.LogMessage("Exiting...")
        wx.LogMessage("%s %s" % (self.GetSize(), self.GetPosition()))

        config = configparser.ConfigParser()
        config.add_section('window')
        x, y = self.GetSize()
        config.set('window', 'sizeX', x)
        config.set('window', 'sizeY', y)
        x, y = self.GetPosition()
        config.set('window', 'posX', x)
        config.set('window', 'posY', y)
        fout = file('GeniControl.cfg', 'w')
        # os.path.abspath(os.path.expanduser('~/.GeniControl.cfg'))
        config.write(fout)
        fout.close()

        self.Destroy()


def loadConfiguration():
    pass

def saveConfiguration():
    pass

class GeniControlApp(wx.PySimpleApp):
    def __init__(self, model, controller):
        super(GeniControlApp, self).__init__()
        self.model = model
        self.controller = controller

def main():
    app = GeniControlApp(NullModel, None)
    frame = GBFrame(None)

    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()

