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

__all__ = ['DataitemConfiguration']

import wx
import genicontrol.controlids as controlids


MEAS_VALUES = (
    (u'speed_hi',       u'Speed',           u'rpm',     controlids.ID_MEAS_SPEED, controlids.ID_MEAS_SPEED_UNIT),
    (u'h',              u'Head',            u'm',       controlids.ID_MEAS_HEAD, controlids.ID_MEAS_HEAD_UNIT),
    (u'energy_hi',      u'Energy',          u'kWh',     controlids.ID_MEAS_ENERGY, controlids.ID_MEAS_ENERGY_UNIT),
    (u't_2hour_hi',     u'Hours',           u'h',       controlids.ID_MEAS_HOURS, controlids.ID_MEAS_HOURS_UNIT),
    (u'f_act',          u'Performance',     u'%',       controlids.ID_MEAS_PERFORMANCE, controlids.ID_MEAS_PERFORMANCE_UNIT),
    (u'unit_family',    u'Unit family code', u'',       None, None),
    (u'unit_type',      u'Unit type code',   u'',       None, None)
)
MEAS_VALUES_16BIT = (
    (u'power_16',       u'Power',           u'W',       controlids.ID_MEAS_POWER, controlids.ID_MEAS_POWER_UNIT),
    (u't_w_16',         u'Temperature',     u'\xb0C',   controlids.ID_MEAS_TEMPERATURE, controlids.ID_MEAS_TEMPERATURE_UNIT),
    (u'diff_press_16',  u'Diff.pressure',   u'mbar',    controlids.ID_MEAS_DIFFPRESSURE, controlids.ID_MEAS_DIFFPRESSURE_UNIT),
    (u'flow_16',        u'Flowrate',        u'm\u00b3/h',controlids.ID_MEAS_FLOW, controlids.ID_MEAS_FLOW_UNIT)
)

MEAS_VALUES_DICT = dict([(key, (desc, unit, a, b)) for key, desc, unit, a, b in MEAS_VALUES])

MEAS_VALUES_DICT_16BIT = dict([(key, (desc, unit, a, b)) for key, desc, unit, a, b in MEAS_VALUES_16BIT])

REF_VALUES = (
    (u'ref_rem', u'Remote reference (GENIbus setpoint)',               u'%',controlids.ID_REF_REM, controlids.ID_REF_REM_UNIT),
    (u'ref_ir',  u'Infrared controller reference (GENIlink setpoint)', u'%',controlids.ID_REF_IR, controlids.ID_REF_IR_UNIT),
    (u'ref_act', u'Actual reference',                                  u'%',controlids.ID_REF_ACT, controlids.ID_REF_ACT_UNIT),
    (u'sys_fb',  u'System feedback',                                   u'm',controlids.ID_SYS_FB, controlids.ID_SYS_FB_UNIT),
    (u'r_min',   u'Reference subinterval minimum',                     u'%',controlids.ID_R_MIN, controlids.ID_R_MIN_UNIT),
    (u'r_max',   u'Reference subinterval maximum',                     u'%',controlids.ID_R_MAX, controlids.ID_R_MAX_UNIT)
)

REFERENCES_DICT = dict([(key, (desc, unit, a, b)) for key, desc, unit, a, b in REF_VALUES])

PARAMETERS = (
    (u'unit_addr',          u'Busunit address', u'No', controlids.ID_PARAM_UNIT_ADDR, controlids.ID_PARAM_UNIT_ADDR_UNIT),
    (u'group_addr',         u'Group address',   u'No', controlids.ID_PARAM_GROUP_ADDR, controlids.ID_PARAM_GROUP_ADDR_UNIT),
    (u'h_const_ref_min',    u'Const. pressure min. reference', u'%', controlids.ID_PARAM_H_CONST_REF_MIN, controlids.ID_PARAM_H_CONST_REF_MIN_UNIT),
    (u'h_const_ref_max',    u'Const. pressure max. reference', u'%', controlids.ID_PARAM_H_CONST_REF_MAX, controlids.ID_PARAM_H_CONST_REF_MAX_UNIT),
    (u'h_prop_ref_min',     u'Prop. pressure min. reference', u'%', controlids.ID_PARAM_H_PROP_REF_MIN, controlids.ID_PARAM_H_PROP_REF_MIN_UNIT),
    (u'h_prop_ref_max',     u'Prop. pressure max. reference', u'%', controlids.ID_PARAM_H_PROP_REF_MAX, controlids.ID_PARAM_H_PROP_REF_MAX_UNIT)
)

PARAMETERS_DICT = dict([(key, (desc, unit, a, b)) for key, desc, unit, a, b in PARAMETERS])

STRING_VALUES = (
    (u"product_name",    u"Product name"      , controlids.ID_STR_PRODUCT_NAME),
    (u"software_name1",  u"Software name"     , controlids.ID_STR_SOFTWARE_NAME1),
    (u"compile_date1",   u"Compilation date"  , controlids.ID_STR_COMPILE_DATE1),
    (u"protocol_code",   u"Protocol code"     , controlids.ID_STR_PROTOCOL_CODE),
    (u"developers",      u"Developers"        , controlids.ID_STR_DEVELOPERS),
    (u"serial_no",       u"Serial No."        , controlids.ID_STR_SERIAL_NO)
)

INFO_VALUES = (
    u"t_2hour_hi",
    u"t_2hour_lo",
    u"f_act",
    u"speed_hi",
    u"speed_lo",
    u"h",
    u"q",
    u"p",
    u"t_w",
    u"t_m",
    u"t_e",
    u"i_mo",
    u"v_dc",
    u"power_16",
    u"energy_hi",
    u"energy_lo",
    u"diff_press_16",
    u"flow_16",
    u"t_w_16",
    u"ref_rem",
    u"ref_ir",
    u"ref_act",
    u"h_prop_ref_min",
    u"h_prop_ref_max",
    u"h_const_ref_max",
    u"h_const_ref_min",
    u"sys_fb",
    u"r_min",
    u"r_max",
    u"group_addr",
    u"unit_addr",
    u"led_contr",
    u"start_alarm1",
    u"qsd_alarm1",
    u"stop_alarm1",
    u"surv_alarm1",
    u"ind_alarm",
    u"act_mode1",
    u"act_mode2",
    u"act_mode3",
    u"contr_source",
    u"unit_family",
    u"unit_type",
    u"unit_version",
    u"alarm_code",
    u"alarm_code_disp",
    u"alarm_log_1",
    u"alarm_log_2",
    u"alarm_log_3",
    u"alarm_log_4",
    u"alarm_log_5"
)

DataitemConfiguration = {
    "MeasurementValues":    MEAS_VALUES,
    "ReferenceValues":      REF_VALUES,
    "StringValues":         STRING_VALUES,
    "InfoValues":           INFO_VALUES,
    "Parameters":           PARAMETERS,
    "MeasurementValues16bit": MEAS_VALUES_16BIT
}
