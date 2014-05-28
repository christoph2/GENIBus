#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

__all__ = [
    'COMMANDS', 'MEASUREMENT_VALUES', 'REFERENCES', 'PARAMETER', 'STRINGS',
    'DATAITEMS', 'defs.ACC_RO', 'defs.ACC_WO', 'defs.ACC_WR'
]

from collections import namedtuple
import genicontrol.defs as defs


Dataitem = namedtuple('Dataitem', 'name klass id access note')

DATAITEMS = (
    Dataitem(u"df_buf_len",                         0,   2, defs.ACC_RO,   u""),
    Dataitem(u"unit_bus_mode",                      0,   3, defs.ACC_RO,   u""),
    Dataitem(u"t_2hour_hi",                         2,  24, defs.ACC_RO,   u"Two hour counter"                                         ),
    Dataitem(u"t_2hour_lo",                         2,  25, defs.ACC_RO,   u"Two hour counter"                                         ),
    Dataitem(u"i_dc",                               2,  26, defs.ACC_RO,   u"Frequency converter DC link current"                      ),
    Dataitem(u"v_dc",                               2,  27, defs.ACC_RO,   u"Frequency converter DC link voltage"                      ),
    Dataitem(u"t_e",                                2,  28, defs.ACC_RO,   u"Temperature in contdefs.ACC_ROl electdefs.ACC_ROnics"     ),
    Dataitem(u"t_m",                                2,  29, defs.ACC_RO,   u"Temp. in motor or in frequency converter module"          ),
    Dataitem(u"i_mo",                               2,  30, defs.ACC_RO,   u"Motor current"                                            ),
    Dataitem(u"i_line",                             2,  31, defs.ACC_RO,   u"Mains supply current"                                     ),
    Dataitem(u"f_act",                              2,  32, defs.ACC_RO,   u"Actual control signal (freq. or voltage) applied to pump" ),
    Dataitem(u"p",                                  2,  34, defs.ACC_RO,   u"Power consumption"                                        ),
    Dataitem(u"speed",                              2,  35, defs.ACC_RO,   u"Pump speed"                                               ),
    Dataitem(u"h",                                  2,  37, defs.ACC_RO,   u"Actual pump head"                                         ),
    Dataitem(u"q",                                  2,  39, defs.ACC_RO,   u"Actual pump flow"                                         ),
    Dataitem(u"ref_loc",                            2,  40, defs.ACC_RO,   u"Local reference setting"                                  ),
    Dataitem(u"p_max",                              2,  41, defs.ACC_RO,   u"Maximum power consumption"                                ),
    Dataitem(u"q_kn1",                              2,  42, defs.ACC_RO,   u"Minimum possible flow at maximum power consum."           ),
    Dataitem(u"q_max",                              2,  43, defs.ACC_RO,   u"Maximum possible flow at maximum power consum."           ),
    Dataitem(u"h_max",                              2,  44, defs.ACC_RO,   u"Maximum pump head (closed valve)"                         ),
    Dataitem(u"ind_alarm_bak",                      2,  46, defs.ACC_RO,   u"Back up byte to indication alarm"                         ),
    Dataitem(u"led_contr",                          2,  47, defs.ACC_RO,   u"Status of green and red indication diodes"                ),
    Dataitem(u"ref_act",                            2,  48, defs.ACC_RO,   u"Actual reference"                                         ),
    Dataitem(u"ref_inf",                            2,  49, defs.ACC_RO,   u"Reference influence"                                      ),
    Dataitem(u"t_w",                                2,  58, defs.ACC_RO,   u"Water temperature"                                        ),
    Dataitem(u"ref_att_loc",                        2,  61, defs.ACC_RO,   u"Local reference attenuator input"                         ),
    Dataitem(u"sys_ref",                            2,  62, defs.ACC_RO,   u"Selected system control loop reference"                   ),
    Dataitem(u"start_alarm1",                       2,  64, defs.ACC_RO,   u"Start Alarm No. 1"                                        ),
    Dataitem(u"start_alarm2",                       2,  65, defs.ACC_RO,   u"Start Alarm No. 2"                                        ),
    Dataitem(u"qsd_alarm1",                         2,  66, defs.ACC_RO,   u"Quick Shut Down Alarm No. 1"                              ),
    Dataitem(u"qsd_alarm2",                         2,  67, defs.ACC_RO,   u"Quick Shut Down Alarm No. 2"                              ),
    Dataitem(u"stop_alarm1",                        2,  68, defs.ACC_RO,   u"Stop Alarm No. 1"                                         ),
    Dataitem(u"stop_alarm2",                        2,  69, defs.ACC_RO,   u"Stop Alarm No. 2"                                         ),
    Dataitem(u"surv_alarm1",                        2,  70, defs.ACC_RO,   u"Survive Alarm No. 1"                                      ),
    Dataitem(u"surv_alarm2",                        2,  71, defs.ACC_RO,   u"Survive Alarm No. 2"                                      ),
    Dataitem(u"ind_alarm",                          2,  72, defs.ACC_RO,   u"Indication Alarm"                                         ),
    Dataitem(u"start_alarm1_bak",                   2,  73, defs.ACC_RO,   u"Start Alarm No. 1 backup"                                 ),
    Dataitem(u"start_alarm2_bak",                   2,  74, defs.ACC_RO,   u"Start Alarm No. 2 backup"                                 ),
    Dataitem(u"qsd_alarm1_bak",                     2,  75, defs.ACC_RO,   u"Quick Shut Down Alarm No. 1 backup"                       ),
    Dataitem(u"qsd_alarm2_bak",                     2,  76, defs.ACC_RO,   u"Quick Shut Down Alarm No. 2 backup"                       ),
    Dataitem(u"stop_alarm1_bak",                    2,  77, defs.ACC_RO,   u"Stop Alarm No. 1 backup"                                  ),
    Dataitem(u"stop_alarm2_bak",                    2,  78, defs.ACC_RO,   u"Stop Alarm No. 2 backup"                                  ),
    Dataitem(u"surv_alarm1_bak",                    2,  79, defs.ACC_RO,   u"Survive Alarm No.1 backup"                                ),
    Dataitem(u"surv_alarm2_bak",                    2,  80, defs.ACC_RO,   u"Survive Alarm No.2 backup"                                ),
    Dataitem(u"act_mode1",                          2,  81, defs.ACC_RO,   u"Actual Mode Status No. 1"                                 ),
    Dataitem(u"act_mode2",                          2,  82, defs.ACC_RO,   u"Actual Mode Status No. 2"                                 ),
    Dataitem(u"act_mode3",                          2,  83, defs.ACC_RO,   u"Actual Mode Status No. 3"                                 ),
    Dataitem(u"loc_setup1",                         2,  85, defs.ACC_RO,   u"Local setup"                                              ),
    Dataitem(u"rem_setup1",                         2,  87, defs.ACC_RO,   u"Remote setup"                                             ),
    Dataitem(u"extern_inputs",                      2,  89, defs.ACC_RO,   u"Logical value of all external control inputs"             ),
    Dataitem(u"contr_source",                       2,  90, defs.ACC_RO,   u"Currently active contr. source and priority"              ),
    Dataitem(u"stop_alarm3",                        2,  93, defs.ACC_RO,   u"Stop Alarm No. 3"                                         ),
    Dataitem(u"stop_alarm3_bak",                    2,  96, defs.ACC_RO,   u"Stop Alarm No. 3 backup"                                  ),
    Dataitem(u"curve_no_ref",                       2,  97, defs.ACC_RO,   u"Selected curve No. (LED bar indicator No.)"               ),
    Dataitem(u"contr_ref",                          2, 147, defs.ACC_RO,   u"Control loop reference"                                   ),
    Dataitem(u"unit_family",                        2, 148, defs.ACC_RO,   u"Unit family code"                                         ),
    Dataitem(u"unit_type",                          2, 149, defs.ACC_RO,   u"Unit type code"                                           ),
    Dataitem(u"unit_version",                       2, 150, defs.ACC_RO,   u"Unit version code"                                        ),
    Dataitem(u"energy_hi",                          2, 152, defs.ACC_RO,   u"Accumulated electric energy consumption"                  ),
    Dataitem(u"energy_lo",                          2, 153, defs.ACC_RO,   u"Accumulated electric energy consumption"                  ),
    Dataitem(u"alarm_code_disp",                    2, 155, defs.ACC_RO,   u"Interpreted (filtered) version of alarm_code"             ),
    Dataitem(u"alarm_code",                         2, 158, defs.ACC_RO,   u"Actual alarm"                                             ),
    Dataitem(u"alarm_log_1",                        2, 159, defs.ACC_RO,   u"Logged alarm code No. 1"                                  ),
    Dataitem(u"alarm_log_2",                        2, 160, defs.ACC_RO,   u"Logged alarm code No. 2"                                  ),
    Dataitem(u"alarm_log_3",                        2, 161, defs.ACC_RO,   u"Logged alarm code No. 3"                                  ),
    Dataitem(u"alarm_log_4",                        2, 162, defs.ACC_RO,   u"Logged alarm code No. 4"                                  ),
    Dataitem(u"alarm_log_5",                        2, 163, defs.ACC_RO,   u"Logged alarm code No. 5"                                  ),
    Dataitem(u"twin_pump_mode",                     2, 166, defs.ACC_RO,   u"Twin Pump Mode, UPED's only"                              ),

    Dataitem(u"RESET",                              3,   1, defs.ACC_WO,   u"Hardware resets the pump"                                 ),
    Dataitem(u"RESET_ALARM",                        3,   2, defs.ACC_WO,   u"Resets pending alarm and attempts a restart"              ),
    Dataitem(u"USER_BOOT",                          3,   4, defs.ACC_WO,   u"Returns to factory setting. Pump must be stopped"         ),
    Dataitem(u"STOP",                               3,   5, defs.ACC_WO,   u"Stops the pump (Operation Mode Stop)"                     ),
    Dataitem(u"START",                              3,   6, defs.ACC_WO,   u"Starts the pump (Operation Mode Start)"                   ),
    Dataitem(u"REMOTE",                             3,   7, defs.ACC_WO,   u"Switch to Remote Mode"                                    ),
    Dataitem(u"LOCAL",                              3,   8, defs.ACC_WO,   u"Switch to Local Mode"                                     ),
    Dataitem(u"RUN",                                3,   9, defs.ACC_WO,   u"Run Mode, only for factory use"                           ),
    Dataitem(u"PROGRAM",                            3,  10, defs.ACC_WO,   u"Programming Mode, only for factory use"                   ),
    Dataitem(u"CONST_FREQ",                         3,  22, defs.ACC_WO,   u"Sets the pump in Control Mode Const. Frequency"           ),
    Dataitem(u"PROP_PRESS",                         3,  23, defs.ACC_WO,   u"Sets the pump in Control Mode Proportional Press."        ),
    Dataitem(u"CONST_PRESS",                        3,  24, defs.ACC_WO,   u"Sets the pump in Control Mode Constant Pressure"          ),
    Dataitem(u"MIN",                                3,  25, defs.ACC_WO,   u"Pump running on min. curve (Operation Mode Min)"          ),
    Dataitem(u"MAX",                                3,  26, defs.ACC_WO,   u"Pump running on max. curve (Oper. Mode Max)"              ),
    Dataitem(u"INFLUENCE_E",                        3,  28, defs.ACC_WO,   u"Enables temperature influence"                            ),
    Dataitem(u"INFLUENCE_D",                        3,  29, defs.ACC_WO,   u"Enables temperature influence"                            ),
    Dataitem(u"LOCK_KEYS",                          3,  30, defs.ACC_WO,   u"Keys Setting is Locked (buttons at pump disabled)"        ),
    Dataitem(u"UNLOCK_KEYS",                        3,  31, defs.ACC_WO,   u"Keys Setting is Unlocked (buttons at pump enabled)"       ),
    Dataitem(u"REF_UP",                             3,  33, defs.ACC_WO,   u"Increases setpoint one step, like pressing + button"      ),
    Dataitem(u"REF_DOWN",                           3,  34, defs.ACC_WO,   u"Decreases setpoint one step, like pressing - button"      ),
    Dataitem(u"RESET_HIST",                         3,  36, defs.ACC_WO,   u"Resets kWh- and h-counter. Pump must be stopped"          ),
    Dataitem(u"RESET_ALARM_LOG",                    3,  51, defs.ACC_WO,   u"Resets the alarm log"                                     ),
    Dataitem(u"AUTOMATIC",                          3,  52, defs.ACC_WO,   u"Sets the pump in Control Mode Automatic"                  ),
    Dataitem(u"TWIN_MODE_SPARE",                    3,  58, defs.ACC_WO,   u"Twin Pump Mode Spare"                                     ),
    Dataitem(u"TWIN_MODE_ALT",                      3,  59, defs.ACC_WO,   u"Twin Pump Mode Alternating"                               ),
    Dataitem(u"TWIN_MODE_SYNC",                     3,  60, defs.ACC_WO,   u"Twin Pump Mode Syncrouneous"                              ),
    Dataitem(u"NIGHT_REDUCT_E+",                    3,  66, defs.ACC_WO,   u"Enables Night Reduction"                                  ),
    Dataitem(u"NIGHT_REDUCT_D+",                    3,  67, defs.ACC_WO,   u"Disables Night Reduction"                                 ),

    Dataitem(u"unit_addr",                          4,  46, defs.ACC_WR,   u"GENIbus/GENIlink unit address"                            ),
    Dataitem(u"group_addr",                         4,  47, defs.ACC_WR,   u"GENIbus group address"                                    ),
    Dataitem(u"min_curve_no",                       4,  74, defs.ACC_WR,   u"Minimum curve No."                                        ),
    Dataitem(u"h_const_ref_min",                    4,  83, defs.ACC_WR,   u"Constant Pressure Mode minimum reference"                 ),
    Dataitem(u"h_const_ref_max",                    4,  84, defs.ACC_WR,   u"Constant Pressure Mode maximum reference"                 ),
    Dataitem(u"h_prop_ref_min",                     4,  85, defs.ACC_WR,   u"Proportional Pressure Mode minimum reference"             ),
    Dataitem(u"h_prop_ref_max",                     4,  86, defs.ACC_WR,   u"Proportional Pressure Mode maximum reference"             ),
    Dataitem(u"ref_steps",                          4,  87, defs.ACC_WR,   u"No. of discrete reference steps"                          ),

    Dataitem(u"ref_rem",                            5,   1, defs.ACC_WO,   u"GENIbus setpoint (Remote reference)"                      ),
    Dataitem(u"ref_ir",                             5,   2, defs.ACC_WO,   u"GENIlink setpoint (curve No.)"                            ),
    Dataitem(u"ref_att_rem",                        5,  19, defs.ACC_WO,   u"Remote reference attenuation"                             ),

    Dataitem(u"product_name",                       7,   1, defs.ACC_RO,   u""                                                         ),
    Dataitem(u"software_name1",                     7,   3, defs.ACC_RO,   u""                                                         ),
    Dataitem(u"compile_date1",                      7,   4, defs.ACC_RO,   u""                                                         ),
    Dataitem(u"protocol_code",                      7,   5, defs.ACC_RO,   u""                                                         ),
    Dataitem(u"developers",                         7,   7, defs.ACC_RO,   u""                                                         ),
    Dataitem(u"rtos_code",                          7,  12, defs.ACC_RO,   u""                                                         ),
)

def addToDict(d, k, v):
    d[k] = v


PROTOCOL_DATA = dict()
COMMANDS = dict()
MEASUREMENT_VALUES = dict()
REFERENCES = dict()
PARAMETER = dict()
STRINGS = dict()


for item in DATAITEMS:
    if item.klass == 0:
        addToDict(PROTOCOL_DATA, item.name, item)
    elif item.klass == 2:
        addToDict(MEASUREMENT_VALUES, item.name, item)
    elif item.klass == 3:
        addToDict(COMMANDS, item.name, item)
    elif item.klass == 4:
        addToDict(PARAMETER, item.name, item)
    elif item.klass == 5:
        addToDict(REFERENCES, item.name, item)
    elif item.klass == 7:
        addToDict(STRINGS, item.name, item)

DATAITEMS_FOR_CLASS = {
    defs.ADPUClass.PROTOCOL_DATA:               PROTOCOL_DATA,
    defs.ADPUClass.MEASURERED_DATA:             MEASUREMENT_VALUES,
    defs.ADPUClass.COMMANDS:                    COMMANDS,
    defs.ADPUClass.CONFIGURATION_PARAMETERS:    PARAMETER,
    defs.ADPUClass.REFERENCE_VALUES:            REFERENCES,
    defs.ADPUClass.ASCII_STRINGS:               STRINGS
}

dataItemsById = lambda klass : dict([(v[2], (k, v[3], v[4])) for k, v in DATAITEMS_FOR_CLASS[klass].items()])
dataItemsByName = lambda klass : dict([(k, (v[2], v[3], v[4])) for k, v in DATAITEMS_FOR_CLASS[klass].items()])

DATAITEMS_BY_ID = {
    defs.ADPUClass.PROTOCOL_DATA:               dataItemsById(defs.ADPUClass.PROTOCOL_DATA),
    defs.ADPUClass.MEASURERED_DATA:             dataItemsById(defs.ADPUClass.MEASURERED_DATA),
    defs.ADPUClass.COMMANDS:                    dataItemsById(defs.ADPUClass.COMMANDS),
    defs.ADPUClass.CONFIGURATION_PARAMETERS:    dataItemsById(defs.ADPUClass.CONFIGURATION_PARAMETERS),
    defs.ADPUClass.REFERENCE_VALUES:            dataItemsById(defs.ADPUClass.REFERENCE_VALUES),
    defs.ADPUClass.ASCII_STRINGS:               dataItemsById(defs.ADPUClass.ASCII_STRINGS),
}

DATAITEMS_BY_NAME = {
    defs.ADPUClass.PROTOCOL_DATA:               dataItemsByName(defs.ADPUClass.PROTOCOL_DATA),
    defs.ADPUClass.MEASURERED_DATA:             dataItemsByName(defs.ADPUClass.MEASURERED_DATA),
    defs.ADPUClass.COMMANDS:                    dataItemsByName(defs.ADPUClass.COMMANDS),
    defs.ADPUClass.CONFIGURATION_PARAMETERS:    dataItemsByName(defs.ADPUClass.CONFIGURATION_PARAMETERS),
    defs.ADPUClass.REFERENCE_VALUES:            dataItemsByName(defs.ADPUClass.REFERENCE_VALUES),
    defs.ADPUClass.ASCII_STRINGS:               dataItemsByName(defs.ADPUClass.ASCII_STRINGS),
}

import yaml

#yaml.dump(DATAITEMS, open(r'C:\Users\christoph303\Documents\Arduino\libraries\Genibus\tools\genicontrol\config\dataitems.yaml', 'w'))

"""
Code Alarm Group Alarm Cause
2  Missing Phase
32 Overvoltage
40 Undervoltage
48 Overload
49 Overcurrent (i_line, i_dc, i_mo)
51 Blocked motor/pump
56 Underload
57 Dry Running
58 Low Flow
64 Overtemperature
65 Motor Temperature (t_m)
66 Control Electronics Temperature (t_e)
67 Power Converter Temperature (t_m)
68 External Temperature / Water Temperature (t_w)
72 Hardware Fault type 1
73 Hardware Shut Down (HSD)
74 Internal Supply Voltage too high
75 Internal Supply Voltage too low
76 Internal Communication failure
77 Twin Pump Communication failure
152 Add On Module Communication Fault
80 Hardware Fault type 2
83 FE Parameter Area Verification error (EEPROM)
85 BE Parameter Area Verification error (EEPROM)
88 Sensor Fault
89 (Feedback) Sensor 1 signal fault
90 RPM Sensor signal fault
91 Temperature Sensor signal fault
92 (Feedback) Sensor calibration fault
"""

