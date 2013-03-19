#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2012 by Christoph Schueler <github.com/Christoph2,
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
ID_CMD_RESET_ALARM          = wx.NewId()
ID_CMD_RESET_ALARM_LOG      = wx.NewId()

ID_MEAS_SPEED               = wx.NewId()
ID_MEAS_HEAD                = wx.NewId()
ID_MEAS_FLOW                = wx.NewId()
ID_MEAS_POWER               = wx.NewId()
ID_MEAS_ENERGY              = wx.NewId()
ID_MEAS_HOURS               = wx.NewId()
ID_MEAS_PERFORMACE          = wx.NewId()

ID_MEAS_SPEED_UNIT          = wx.NewId()
ID_MEAS_HEAD_UNIT           = wx.NewId()
ID_MEAS_FLOW_UNIT           = wx.NewId()
ID_MEAS_POWER_UNIT          = wx.NewId()
ID_MEAS_ENERGY_UNIT         = wx.NewId()
ID_MEAS_HOURS_UNIT          = wx.NewId()
ID_MEAS_PERFORMACE_UNIT     = wx.NewId()

ID_OPERATION_MODE           = wx.NewId()
ID_SYSTEM_MODE              = wx.NewId()
ID_CONTROL_SOURCE           = wx.NewId()
ID_EXT_ANALOGUE             = wx.NewId()
ID_TOTAL_INFLUENCE          = wx.NewId()
ID_SETPOINT                 = wx.NewId()
ID_ACTUAL_SETPOINT          = wx.NewId()

ID_ALARM_ACTUAL             = wx.NewId()
ID_ALARM_LOG1               = wx.NewId()
ID_ALARM_LOG2               = wx.NewId()
ID_ALARM_LOG3               = wx.NewId()
ID_ALARM_LOG4               = wx.NewId()
ID_ALARM_LOG5               = wx.NewId()

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
