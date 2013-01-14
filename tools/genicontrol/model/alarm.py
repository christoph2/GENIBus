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

from collections import namedtuple

AlarmDescription = namedtuple('AlarmDescription', 'lowLewelDescription highLevelDescription')

##
## Current and logged alarms.
##

## Alarms preventing the UPE pump from starting.

# start_alarm1 (2, 64 / -), start_alarm1_bak (2, 73 / 56).
V_DC_MAX_ST_ERR     = 0x01
V_DC_MIN_ST_ERR     = 0x02
V_SUPP_MAX_ST_ERR   = 0x04
V_SUPP_MIN_ST_ERR   = 0x08
T_M_ST_ERR          = 0x10
T_E_ST_ERR          = 0x20
T_W_ST_ERR          = 0x40
HW_ST_ERR           = 0x80

START_ALARM1_DESCRIPTIONS = {
    V_DC_MAX_ST_ERR:    AlarmDescription("DC link voltage too high", "Voltage high"),
    V_DC_MIN_ST_ERR:    AlarmDescription("DC link voltage too low", "Voltage low"),
    V_SUPP_MAX_ST_ERR:  AlarmDescription("Internal supply voltage too high", "Fault in electronics"),
    V_SUPP_MIN_ST_ERR:  AlarmDescription("Internal supply voltage too low", "Fault in electronics"),
    T_M_ST_ERR:         AlarmDescription("Motor temperature too high", "Pump temperature high"),
    T_E_ST_ERR:         AlarmDescription("Electronics temperature too high", "Pump temperature high"),
    T_W_ST_ERR:         AlarmDescription("Water temperature too high", "Water temperature high"),
    HW_ST_ERR:          AlarmDescription("Hardware fault", "Fault in electronics"),
}

# start_alarm2 (2, 65 / -),  start_alarm2_bak (2, 74 / 57).
V_RIP_ST_ERR        = 0x01
V_LINE_MAX_ST_ERR   = 0x02
V_LINE_MIN_ST_ERR   = 0x04
SW_ST_ERR           = 0x08
I_LEAK_ERR          = 0x10

START_ALARM2_DESCRIPTIONS = {
    V_RIP_ST_ERR:       AlarmDescription("DC link ripple curr. too high", "Missing phase"),
    V_LINE_MAX_ST_ERR:  AlarmDescription("Line voltage too high", "Voltage high"),
    V_LINE_MIN_ST_ERR:  AlarmDescription("Line voltage too low", "Voltage low"),
    SW_ST_ERR:          AlarmDescription("Software verification error", "Fault in electronics"),
    I_LEAK_ERR:         AlarmDescription("Leakage current too high", "Leakage current"),
}

## Alarms effecting a Quick Shut Down of the power electronics, pump stops.

# qsd_alarm1 (2, 66 / -), qsd_alarm1_bak (2, 75 / 58).
V_DC_MAX_QSD_ERR    = 0x01
V_DC_MIN_QSD_ERR    = 0x02
V_SUPP_MAX_QSD_ERR  = 0x04
V_SUPP_MAX_QSD_ERR  = 0x08
I_FAULT_QSD_ERR     = 0x10
FAULT_ERR           = 0x20
HSD_ERR             = 0x40

QSD_DESCRIPTIONS = {
    V_DC_MAX_QSD_ERR:   AlarmDescription("DC link voltage too high", "Voltage high"),
    V_DC_MIN_QSD_ERR:   AlarmDescription("DC link voltage too low", "Voltage low"),
    V_SUPP_MAX_QSD_ERR: AlarmDescription("Internal supply voltage too high", "Fault in electronics"),
    V_SUPP_MAX_QSD_ERR: AlarmDescription("Internal supply voltage too low", "Fault in electronics"),
    I_FAULT_QSD_ERR:    AlarmDescription("Current too high", "Overcurrent/Blocked pump"),
    FAULT_ERR:          AlarmDescription("Hardware fault signal", "Fault in electronics"),
    HSD_ERR:            AlarmDescription("Hardware fault", "Fault in electronics"),
}

## Alarms effecting a stop of the pump.

# stop_alarm1 (2, 68 / -), stop_alarm1_bak (2, 77 / 60).
V_RIP_STOP_ERR  = 0x01
BLOCKED_ERR     = 0x02
I_DC_STOP_ERR   = 0x04
I_MO_STOP_ERR   = 0x08
T_M_STOP_ERR    = 0x10
T_E_STOP_ERR    = 0x20
T_W_STOP_ERR    = 0x40
MPF_STOP_ERR    = 0x80

STOP_ALARM1_DESCRIPTIONS = {
    V_RIP_STOP_ERR:     AlarmDescription("DC link ripple current too high", "Missing phase"),
    BLOCKED_ERR:        AlarmDescription("pump/motor blocked", "Overcurrent/Blocked pump"),
    I_DC_STOP_ERR:      AlarmDescription("DC link current too high", "Overcurrent/Blocked pump"),
    I_MO_STOP_ERR:      AlarmDescription("Motor current too high", "Overcurrent/Blocked pump"),
    T_M_STOP_ERR:       AlarmDescription("Motor temperature too high", "Pump temperature high"),
    T_E_STOP_ERR:       AlarmDescription("Electronics temperature too high", "Pump temperature high"),
    T_W_STOP_ERR:       AlarmDescription("Water temperature too high", "Water temperature high"),
    MPF_STOP_ERR:       AlarmDescription("Motor Protection Func. active", "Overcurrent/Blocked pump"),
}

# stop_alarm2 (2, 69 / -), stop_alarm2_bak (2, 78 / 61).
FB_SIG_STOP_ERR     = 0x01
REF_SIG_STOP_ERR    = 0x02
I_FAULT_STOP_ERR    = 0x08
INT_COM_STOP_ERR    = 0x10
RPM_MEAS_STOP_ERR   = 0x20
SLIP_STOP_ERR       = 0x40

STOP_ALARM2_DESCRIPTIONS = {
    FB_SIG_STOP_ERR:    AlarmDescription("Feed back signal error", "Sensor fault"),
    REF_SIG_STOP_ERR:   AlarmDescription("Reference signal error", "Setpoint signal fault"),
    I_FAULT_STOP_ERR:   AlarmDescription("Current too high", "Overcurrent/Blocked pump"),
    INT_COM_STOP_ERR:   AlarmDescription("Internal communication error", "Fault in electronics"),
    RPM_MEAS_STOP_ERR:  AlarmDescription("rpm measurement error", "Fault in electronics"),
    SLIP_STOP_ERR:      AlarmDescription("Motor slip too high", "Overcurrent/Blocked pump"),
}

# stop_alarm3 (2, 93 / -), stop_alarm3_bak (2, 96 / 64).
DRY_RUN_ERR         = 0x02
EE_STOP_ERR         = 0x04

STOP_ALARM3_DESCRIPTIONS = {
    DRY_RUN_ERR:        AlarmDescription("Too low current consumption", "Dry running"),
    EE_STOP_ERR:        AlarmDescription("Check sum error in EEPROM", "Fault in electronics"),
}

## Alarms effecting a survive action of the pump.

# surv_alarm1 (2, 70 / -), surv_alarm1_bak (2, 79 / 62).
HW_SURV_ERR         = 0x01

SURV_ALARM1_DESCRIPTIONS = {
    HW_SURV_ERR:        AlarmDescription("Hardware survive error", "Fault in electronics"),
}

# surv_alarm2 (2, 71 / -), surv_alarm2_bak (2, 80 / 63).
FB_SIG_SURV_ERR      = 0x08
RPM_MEAS_SURV_ERR    = 0x20
TWIN_COMM_ERR        = 0x40


SURV_ALARM2_DESCRIPTIONS = {
    FB_SIG_SURV_ERR:    AlarmDescription("Feedback signal from sensor", "pressure sensor error"),
    RPM_MEAS_SURV_ERR:  AlarmDescription("Signal from rpm sensor", "Fault in electronics"),
    TWIN_COMM_ERR:      AlarmDescription("Twin pump bus connection error", "Twin pump bus connection error"),
}

## Indication only alarms.

# ind_alarm (2, 72 / -), ind_alarm_bak (2, 46 / -).
EE_CHK_ERR          = 0x01
EE_ACC_ERR          = 0x02
PANEL_ERR           = 0x04

IND_ALARM_DESCRIPTIONS = {
    EE_CHK_ERR:         AlarmDescription("Check sum error in EEPROM", "Fault in electronics"),
    EE_ACC_ERR:         AlarmDescription("Access error in EEPROM", "Fault in electronics"),
    PANEL_ERR:          AlarmDescription("Bar graph hardware error", "Fault in electronics"),
}

