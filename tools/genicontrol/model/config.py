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
    (u'q',              u'Flowrate',        u'm3/h',    controlids.ID_MEAS_FLOW, controlids.ID_MEAS_FLOW_UNIT),  ## ³
    (u'p',              u'Power' ,          u'W',       controlids.ID_MEAS_POWER, controlids.ID_MEAS_POWER_UNIT),
    (u'energy_hi',      u'Energy',          u'kWh',     controlids.ID_MEAS_ENERGY, controlids.ID_MEAS_ENERGY_UNIT),
    (u't_2hour_hi',     u'Hours',           u'h',       controlids.ID_MEAS_HOURS, controlids.ID_MEAS_HOURS_UNIT),
    (u'f_act',          u'Performance',     u'%',       controlids.ID_MEAS_PERFORMACE, controlids.ID_MEAS_PERFORMACE_UNIT),

    (u'unit_family',    u'Unit family code', u'',       None, None),
    (u'unit_type',      u'Unit type code',  u'',        None, None),
)

MEAS_VALUES_DICT = dict([(key, (desc, unit, a, b)) for key, desc, unit, a, b in MEAS_VALUES])


REF_VALUES = (
    (u"ref_rem",        u'GENIBus ref.',    u'%'),
    (u'ref_ir',         u'GENIlink ref.',   u'%'),
)

PARAMETERS = (
    (u"unit_addr",          u"Busunit address", "", controlids.ID_PARAM_UNIT_ADDR ),
    (u"group_addr",         u"Group address", "", controlids.ID_PARAM_GROUP_ADDR ),
    (u"h_const_ref_min",    u"Const. pressure min. reference", "", controlids.ID_PARAM_H_CONST_REF_MIN ),
    (u"h_const_ref_max",    u"Const. pressure max. reference", "", controlids.ID_PARAM_H_CONST_REF_MAX ),
    (u"h_prop_ref_min",     u"Prop. pressure min. reference", "", controlids.ID_PARAM_H_PROP_REF_MIN ),
    (u"h_prop_ref_max",     u"Prop. pressure max. reference", "", controlids.ID_PARAM_H_PROP_REF_MAX ),
    #(u"ref_steps",          u"No. of discrete reference steps", controlids.ID_PARAM_REF_STEPS ),
)

STRING_VALUES = (
    (u"product_name",    u"Product name"      , controlids.ID_STR_PRODUCT_NAME),
    (u"software_name1",  u"Software name"     , controlids.ID_STR_SOFTWARE_NAME1),
    (u"compile_date1",   u"Compilation date"  , controlids.ID_STR_COMPILE_DATE1),
    (u"protocol_code",   u"Protocol code"     , controlids.ID_STR_PROTOCOL_CODE),
    (u"developers",      u"Developers"        , controlids.ID_STR_DEVELOPERS),
    (u"serial_no",       u"Serial No."        , controlids.ID_STR_SERIAL_NO),
)

INFO_VALUES = (
    u"t_2hour_hi",
    u"t_2hour_lo",
    u"v_dc",
    u"t_e",
    u"t_m",
    u"i_mo",
    u"f_act",
    u"p",
    u"speed_hi",
    u"speed_lo",
    u"h",
    u"q",
    u"ref_rem",
    u"ref_norm",
    u"ref_ir",
    u"h_prop_ref_min",
    u"h_prop_ref_max",
    u"group_addr",
    u"unit_addr",
    u"h_const_ref_max",
    u"h_const_ref_min",
    u"ref_steps",
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
    u"energy_hi",
    u"energy_lo",
    u"ref_att_loc",
    u"sys_ref",
    u"start_alarm1",
    u"qsd_alarm1",
    u"stop_alarm1",
    u"surv_alarm1",
    u"ind_alarm",
    u"act_mode1",
    u"act_mode2",
    u"act_mode3",
    u"loc_setup1",
    u"rem_setup1",
    u"extern_inputs",
    u"contr_source",
    u"unit_family",
    u"unit_type",
    u"unit_version",
    u"alarm_code_disp",
    u"alarm_code",
    u"alarm_log_1",
    u"alarm_log_2",
    u"alarm_log_3",
    u"alarm_log_4",
    u"alarm_log_5",
    u"curve_no_ref",
)

DataitemConfiguration = {
    "MeasurementValues":    MEAS_VALUES,
    "ReferenceValues":      REF_VALUES,
    "StringValues":         STRING_VALUES,
    "InfoValues":           INFO_VALUES,
    "Parameters":           PARAMETERS
}

