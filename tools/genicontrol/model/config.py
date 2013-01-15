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
    (u'speed',          u'Speed',           u'rpm',     controlids.ID_MEAS_SPEED),
    (u'h',              u'Head',            u'm',       controlids.ID_MEAS_HEAD),
    (u'q',              u'Flowrate',        u'm3/h',    controlids.ID_MEAS_FLOW),  ## ³
    (u'p',              u'Power' ,          u'W',       controlids.ID_MEAS_POWER),
    (u'energy_hi',      u'Energy',          u'kWh',     controlids.ID_MEAS_ENERGY),
    (u't_2hour_hi',     u'Hours',           u'h',       controlids.ID_MEAS_HOURS),
    (u'f_act',          u'Performance',     u'%',       controlids.ID_MEAS_PERFORMACE),
)

REF_VALUES = (
    (u"ref_rem",        u'GENIBus ref.',    u'%'),
    (u'ref_ir',         u'GENIlink ref.',   u'%'),
    (u'ref_att_rem',    u'Ext. Analogue',   u'%'),
)

STRING_VALUES = (
    (u"product_name",    u"Product name"      , controlids.ID_STR_PRODUCT_NAME),
    (u"software_name1",  u"Software name"     , controlids.ID_STR_SOFTWARE_NAME1),
    (u"compile_date1",   u"Compilation date"  , controlids.ID_STR_COMPILE_DATE1),
    (u"protocol_code",   u"Protocol code"     , controlids.ID_STR_PROTOCOL_CODE),
    (u"developers",      u"Developers"        , controlids.ID_STR_DEVELOPERS),
    (u"rtos_code",       u"RTOS code"         , controlids.ID_STR_RTOS_CODE),
)

INFO_VALUES = (
    u"t_2hour_hi",
    u"i_dc",
    u"v_dc",
    u"t_e",
    u"t_m",
    u"i_mo",
    u"i_line",
    u"f_act",
    u"p",
    u"speed",
    u"h",
    u"q",
    u"ref_loc",
    u"p_max",
    u"q_kn1",
    u"q_max",
    u"h_max",
    u"ind_alarm_bak",
    u"led_contr",
    u"ref_act",
    u"ref_inf",
    u"t_w",
    u"ref_att_loc",
    u"sys_ref",
    u"start_alarm1",
    u"start_alarm2",
    u"qsd_alarm1",
    u"qsd_alarm2",
    u"stop_alarm1",
    u"stop_alarm2",
    u"surv_alarm1",
    u"surv_alarm2",
    u"ind_alarm",
    u"start_alarm1_bak",
    u"start_alarm2_bak",
    u"qsd_alarm1_bak",
    u"qsd_alarm2_bak",
    u"stop_alarm1_bak",
    u"stop_alarm2_bak",
    u"surv_alarm1_bak",
    u"surv_alarm2_bak",
    u"act_mode1",
    u"act_mode2",
    u"act_mode3",
    u"loc_setup1",
    u"rem_setup1",
    u"extern_inputs",
    u"contr_source",
    u"stop_alarm3",
    u"stop_alarm3_bak",
    u"curve_no_ref",
    u"contr_ref",
    u"unit_family",
    u"unit_type",
    u"unit_version",
    u"energy_hi",
    u"alarm_code_disp",
    u"alarm_code",
    u"alarm_log_1",
    u"alarm_log_2",
    u"alarm_log_3",
    u"alarm_log_4",
    u"alarm_log_5",
    u"twin_pump_mode",
)

DataitemConfiguration = {
    "MeasurementValues":    MEAS_VALUES,
    "ReferenceValues":      REF_VALUES,
    "StringValues":         STRING_VALUES,
    "InfoValues":           INFO_VALUES
}

