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
    ('speed_hi',       'Speed',           'rpm',     controlids.ID_MEAS_SPEED, controlids.ID_MEAS_SPEED_UNIT),
    ('h',              'Head',            'm',       controlids.ID_MEAS_HEAD, controlids.ID_MEAS_HEAD_UNIT),
    ('energy_hi',      'Energy',          'kWh',     controlids.ID_MEAS_ENERGY, controlids.ID_MEAS_ENERGY_UNIT),
    ('t_2hour_hi',     'Hours',           'h',       controlids.ID_MEAS_HOURS, controlids.ID_MEAS_HOURS_UNIT),
    ('f_act',          'Performance',     '%',       controlids.ID_MEAS_PERFORMANCE, controlids.ID_MEAS_PERFORMANCE_UNIT),
    ('unit_family',    'Unit family code', '',       None, None),
    ('unit_type',      'Unit type code',   '',       None, None)
)
MEAS_VALUES_16BIT = (
    ('power_16',       'Power',           'W',       controlids.ID_MEAS_POWER, controlids.ID_MEAS_POWER_UNIT),
    ('t_w_16',         'Temperature',     '\xb0C',   controlids.ID_MEAS_TEMPERATURE, controlids.ID_MEAS_TEMPERATURE_UNIT),
    ('diff_press_16',  'Diff.pressure',   'mbar',    controlids.ID_MEAS_DIFFPRESSURE, controlids.ID_MEAS_DIFFPRESSURE_UNIT),
    ('flow_16',        'Flowrate',        'm\u00b3/h',controlids.ID_MEAS_FLOW, controlids.ID_MEAS_FLOW_UNIT)
)

MEAS_VALUES_DICT = dict([(key, (desc, unit, a, b)) for key, desc, unit, a, b in MEAS_VALUES])

MEAS_VALUES_DICT_16BIT = dict([(key, (desc, unit, a, b)) for key, desc, unit, a, b in MEAS_VALUES_16BIT])

REF_VALUES = (
    ('ref_rem', 'Remote reference (GENIbus setpoint)',               '%',controlids.ID_REF_REM, controlids.ID_REF_REM_UNIT),
    ('ref_ir',  'Infrared controller reference (GENIlink setpoint)', '%',controlids.ID_REF_IR, controlids.ID_REF_IR_UNIT),
    ('ref_act', 'Actual reference',                                  '%',controlids.ID_REF_ACT, controlids.ID_REF_ACT_UNIT),
    ('sys_fb',  'System feedback',                                   'm',controlids.ID_SYS_FB, controlids.ID_SYS_FB_UNIT),
    ('r_min',   'Reference subinterval minimum',                     '%',controlids.ID_R_MIN, controlids.ID_R_MIN_UNIT),
    ('r_max',   'Reference subinterval maximum',                     '%',controlids.ID_R_MAX, controlids.ID_R_MAX_UNIT)
)

REFERENCES_DICT = dict([(key, (desc, unit, a, b)) for key, desc, unit, a, b in REF_VALUES])

PARAMETERS = (
    ('unit_addr',          'Busunit address', 'No', controlids.ID_PARAM_UNIT_ADDR, controlids.ID_PARAM_UNIT_ADDR_UNIT),
    ('group_addr',         'Group address',   'No', controlids.ID_PARAM_GROUP_ADDR, controlids.ID_PARAM_GROUP_ADDR_UNIT),
    ('h_const_ref_min',    'Const. pressure min. reference', '%', controlids.ID_PARAM_H_CONST_REF_MIN, controlids.ID_PARAM_H_CONST_REF_MIN_UNIT),
    ('h_const_ref_max',    'Const. pressure max. reference', '%', controlids.ID_PARAM_H_CONST_REF_MAX, controlids.ID_PARAM_H_CONST_REF_MAX_UNIT),
    ('h_prop_ref_min',     'Prop. pressure min. reference', '%', controlids.ID_PARAM_H_PROP_REF_MIN, controlids.ID_PARAM_H_PROP_REF_MIN_UNIT),
    ('h_prop_ref_max',     'Prop. pressure max. reference', '%', controlids.ID_PARAM_H_PROP_REF_MAX, controlids.ID_PARAM_H_PROP_REF_MAX_UNIT)
)

PARAMETERS_DICT = dict([(key, (desc, unit, a, b)) for key, desc, unit, a, b in PARAMETERS])

STRING_VALUES = (
    ("product_name",    "Product name"      , controlids.ID_STR_PRODUCT_NAME),
    ("software_name1",  "Software name"     , controlids.ID_STR_SOFTWARE_NAME1),
    ("compile_date1",   "Compilation date"  , controlids.ID_STR_COMPILE_DATE1),
    ("protocol_code",   "Protocol code"     , controlids.ID_STR_PROTOCOL_CODE),
    ("developers",      "Developers"        , controlids.ID_STR_DEVELOPERS),
    ("serial_no",       "Serial No."        , controlids.ID_STR_SERIAL_NO)
)

INFO_VALUES = (
    "t_2hour_hi",
    "t_2hour_lo",
    "f_act",
    "speed_hi",
    "speed_lo",
    "h",
    "q",
    "p",
    "t_w",
    "t_m",
    "t_e",
    "i_mo",
    "v_dc",
    "power_16",
    "energy_hi",
    "energy_lo",
    "diff_press_16",
    "flow_16",
    "t_w_16",
    "ref_rem",
    "ref_ir",
    "ref_act",
    "h_prop_ref_min",
    "h_prop_ref_max",
    "h_const_ref_max",
    "h_const_ref_min",
    "sys_fb",
    "r_min",
    "r_max",
    "group_addr",
    "unit_addr",
    "led_contr",
    "start_alarm1",
    "qsd_alarm1",
    "stop_alarm1",
    "surv_alarm1",
    "ind_alarm",
    "act_mode1",
    "act_mode2",
    "act_mode3",
    "contr_source",
    "unit_family",
    "unit_type",
    "unit_version",
    "alarm_code",
    "alarm_code_disp",
    "alarm_log_1",
    "alarm_log_2",
    "alarm_log_3",
    "alarm_log_4",
    "alarm_log_5"
)

DataitemConfiguration = {
    "MeasurementValues":    MEAS_VALUES,
    "ReferenceValues":      REF_VALUES,
    "StringValues":         STRING_VALUES,
    "InfoValues":           INFO_VALUES,
    "Parameters":           PARAMETERS,
    "MeasurementValues16bit": MEAS_VALUES_16BIT
}
