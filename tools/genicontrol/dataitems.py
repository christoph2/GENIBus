#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['COMMANDS', 'MEASUREMENT_VALUES', 'REFERENCES', 'PARAMETER', 'STRINGS',
           'DATAITEMS', 'ACC_RO', 'ACC_WO', 'ACC_WR']

from collections import namedtuple


ACC_RO  = 0x01
ACC_WO  = 0x02
ACC_WR  = 0x03

Dataitem = namedtuple('Dataitem', 'name klass id access note')

DATAITEMS = (
    Dataitem("t_2hour_hi",                         2,  24, ACC_RO,   "Two hour counter"                                         ),
    Dataitem("t_2hour_lo",                         2,  25, ACC_RO,   "Two hour counter"                                         ),
    Dataitem("i_dc",                               2,  26, ACC_RO,   "Frequency converter DC link current"                      ),
    Dataitem("v_dc",                               2,  27, ACC_RO,   "Frequency converter DC link voltage"                      ),
    Dataitem("t_e",                                2,  28, ACC_RO,   "Temperature in contACC_ROl electACC_ROnics"               ),
    Dataitem("t_m",                                2,  29, ACC_RO,   "Temp. in motor or in frequency converter module"          ),
    Dataitem("i_mo",                               2,  30, ACC_RO,   "Motor current"                                            ),
    Dataitem("i_line",                             2,  31, ACC_RO,   "Mains supply current"                                     ),
    Dataitem("f_act",                              2,  32, ACC_RO,   "Actual control signal (freq. or voltage) applied to pump" ),
    Dataitem("p",                                  2,  34, ACC_RO,   "Power consumption"                                        ),
    Dataitem("speed",                              2,  35, ACC_RO,   "Pump speed"                                               ),
    Dataitem("h",                                  2,  37, ACC_RO,   "Actual pump head"                                         ),
    Dataitem("q",                                  2,  39, ACC_RO,   "Actual pump flow"                                         ),
    Dataitem("ref_loc",                            2,  40, ACC_RO,   "Local reference setting"                                  ),
    Dataitem("p_max",                              2,  41, ACC_RO,   "Maximum power consumption"                                ),
    Dataitem("q_kn1",                              2,  42, ACC_RO,   "Minimum possible flow at maximum power consum."           ),
    Dataitem("q_max",                              2,  43, ACC_RO,   "Maximum possible flow at maximum power consum."           ),
    Dataitem("h_max",                              2,  44, ACC_RO,   "Maximum pump head (closed valve)"                         ),
    Dataitem("ind_alarm_bak",                      2,  46, ACC_RO,   "Back up byte to indication alarm"                         ),
    Dataitem("led_contr",                          2,  47, ACC_RO,   "Status of green and red indication diodes"                ),
    Dataitem("ref_act",                            2,  48, ACC_RO,   "Actual reference"                                         ),
    Dataitem("ref_inf",                            2,  49, ACC_RO,   "Reference influence"                                      ),
    Dataitem("t_w",                                2,  58, ACC_RO,   "Water temperature"                                        ),
    Dataitem("ref_att_loc",                        2,  61, ACC_RO,   "Local reference attenuator input"                         ),
    Dataitem("sys_ref",                            2,  62, ACC_RO,   "Selected system control loop reference"                   ),
    Dataitem("start_alarm1",                       2,  64, ACC_RO,   "Start Alarm No. 1"                                        ),
    Dataitem("start_alarm2",                       2,  65, ACC_RO,   "Start Alarm No. 2"                                        ),
    Dataitem("qsd_alarm1",                         2,  66, ACC_RO,   "Quick Shot Down Alarm No. 1"                              ),
    Dataitem("qsd_alarm2",                         2,  67, ACC_RO,   "Quick Shot Down Alarm No. 2"                              ),
    Dataitem("stop_alarm1",                        2,  68, ACC_RO,   "Stop Alarm No. 1"                                         ),
    Dataitem("stop_alarm2",                        2,  69, ACC_RO,   "Stop Alarm No. 2"                                         ),
    Dataitem("surv_alarm1",                        2,  70, ACC_RO,   "Survive Alarm No. 1"                                      ),
    Dataitem("surv_alarm2",                        2,  71, ACC_RO,   "Survive Alarm No. 2"                                      ),
    Dataitem("ind_alarm",                          2,  72, ACC_RO,   "Indication Alarm"                                         ),
    Dataitem("start_alarm1_bak",                   2,  73, ACC_RO,   "Start Alarm No. 1 backup"                                 ),
    Dataitem("start_alarm2_bak",                   2,  74, ACC_RO,   "Start Alarm No. 2 backup"                                 ),
    Dataitem("qsd_alarm1_bak",                     2,  75, ACC_RO,   "Quick Shot Down Alarm No. 1 backup"                       ),
    Dataitem("qsd_alarm2_bak",                     2,  76, ACC_RO,   "Quick Shot Down Alarm No. 2 backup"                       ),
    Dataitem("stop_alarm1_bak",                    2,  77, ACC_RO,   "Stop Alarm No. 1 backup"                                  ),
    Dataitem("stop_alarm2_bak",                    2,  78, ACC_RO,   "Stop Alarm No. 2 backup"                                  ),
# self.toolTip = toolTip
#locale.setlocale(locale.LC_ALL, ('de_DE', 'UTF8'))

"""
VIEW (the user did something)       --> CONTROLLER
CONTROLLER (change your state)      --> MODEL
CONTROLLER (change your display)    --> VIEW
MODEL (I've changed!)               --> VIEW
VIEW (I need your state information)--> MODEL

MODEL       [Observer  (Observable)]
VIEW        [Composite, Strategy]
CONTROLLER  [Strategy]
"""
    Dataitem("surv_alarm1_bak",                    2,  79, ACC_RO,   "Survive Alarm No.1 backup"                                ),
    Dataitem("surv_alarm2_bak",                    2,  80, ACC_RO,   "Survive Alarm No.2 backup"                                ),
    Dataitem("act_mode1",                          2,  81, ACC_RO,   "Actual Mode Status No. 1"                                 ),
    Dataitem("act_mode2",                          2,  82, ACC_RO,   "Actual Mode Status No. 2"                                 ),
    Dataitem("act_mode3",                          2,  83, ACC_RO,   "Actual Mode Status No. 3"                                 ),
    Dataitem("loc_setup1",                         2,  85, ACC_RO,   "Local setup"                                              ),
    Dataitem("rem_setup1",                         2,  87, ACC_RO,   "Remote setup"                                             ),
    Dataitem("extern_inputs",                      2,  89, ACC_RO,   "Logical value of all external control inputs"             ),
    Dataitem("contr_source",                       2,  90, ACC_RO,   "Currently active contr. source and priority"              ),
    Dataitem("stop_alarm3",                        2,  93, ACC_RO,   "Stop Alarm No. 3"                                         ),
    Dataitem("stop_alarm3_bak",                    2,  96, ACC_RO,   "Stop Alarm No. 3 backup"                                  ),
    Dataitem("curve_no_ref",                       2,  97, ACC_RO,   "Selected curve No. (LED bar indicator No.)"               ),
    Dataitem("contr_ref",                          2, 147, ACC_RO,   "Control loop reference"                                   ),
    Dataitem("unit_family",                        2, 148, ACC_RO,   "Unit family code"                                         ),
    Dataitem("unit_type",                          2, 149, ACC_RO,   "Unit type code"                                           ),
    Dataitem("unit_version",                       2, 150, ACC_RO,   "Unit version code"                                        ),
    Dataitem("energy_hi",                          2, 152, ACC_RO,   "Accumulated electric energy consumption"                  ),
    Dataitem("energy_lo",                          2, 153, ACC_RO,   "Accumulated electric energy consumption"                  ),
    Dataitem("alarm_code_disp",                    2, 155, ACC_RO,   "Interpreted (filtered) version of alarm_code"             ),
    Dataitem("alarm_code",                         2, 158, ACC_RO,   "Actual alarm"                                             ),
    Dataitem("alarm_log_1",                        2, 159, ACC_RO,   "Logged alarm code No. 1"                                  ),
    Dataitem("alarm_log_2",                        2, 160, ACC_RO,   "Logged alarm code No. 2"                                  ),
    Dataitem("alarm_log_3",                        2, 161, ACC_RO,   "Logged alarm code No. 3"                                  ),
    Dataitem("alarm_log_4",                        2, 162, ACC_RO,   "Logged alarm code No. 4"                                  ),
    Dataitem("alarm_log_5",                        2, 163, ACC_RO,   "Logged alarm code No. 5"                                  ),
    Dataitem("twin_pump_mode",                     2, 166, ACC_RO,   "Twin Pump Mode, UPED's only"                              ),

    Dataitem("RESET",                              3,   1, ACC_WO,   "Hardware resets the pump"                                 ),
    Dataitem("RESET_ALARM",                        3,   2, ACC_WO,   "Resets pending alarm and attempts a restart"              ),
    Dataitem("USER_BOOT",                          3,   4, ACC_WO,   "Returns to factory setting. Pump must be stopped"         ),
    Dataitem("STOP",                               3,   5, ACC_WO,   "Stops the pump (Operation Mode Stop)"                     ),
    Dataitem("START",                              3,   6, ACC_WO,   "Starts the pump (Operation Mode Start)"                   ),
    Dataitem("REMOTE",                             3,   7, ACC_WO,   "Switch to Remote Mode"                                    ),
    Dataitem("LOCAL",                              3,   8, ACC_WO,   "Switch to Local Mode"                                     ),
    Dataitem("RUN",                                3,   9, ACC_WO,   "Run Mode, only for factory use"                           ),
    Dataitem("PROGRAM",                            3,  10, ACC_WO,   "Programming Mode, only for factory use"                   ),
    Dataitem("CONST_FREQ",                         3,  22, ACC_WO,   "Sets the pump in Control Mode Const. Frequency"           ),
    Dataitem("PROP_PRESS",                         3,  23, ACC_WO,   "Sets the pump in Control Mode Proportional Press."        ),
    Dataitem("CONST_PRESS",                        3,  24, ACC_WO,   "Sets the pump in Control Mode Constant Pressure"          ),
    Dataitem("MIN",                                3,  25, ACC_WO,   "Pump running on min. curve (Operation Mode Min)"          ),
    Dataitem("MAX",                                3,  26, ACC_WO,   "Pump running on max. curve (Oper. Mode Max)"              ),
    Dataitem("INFLUENCE_E",                        3,  28, ACC_WO,   "Enables temperature influence"                            ),
    Dataitem("INFLUENCE_D",                        3,  29, ACC_WO,   "Enables temperature influence"                            ),
    Dataitem("LOCK_KEYS",                          3,  30, ACC_WO,   "Keys Setting is Locked (buttons at pump disabled)"        ),
    Dataitem("UNLOCK_KEYS",                        3,  31, ACC_WO,   "Keys Setting is Unlocked (buttons at pump enabled)"       ),
    Dataitem("REF_UP",                             3,  33, ACC_WO,   "Increases setpoint one step, like pressing + button"      ),
    Dataitem("REF_DOWN",                           3,  34, ACC_WO,   "Decreases setpoint one step, like pressing - button"      ),
    Dataitem("RESET_HIST",                         3,  36, ACC_WO,   "Resets kWh- and h-counter. Pump must be stopped"          ),
    Dataitem("RESET_ALARM_LOG",                    3,  51, ACC_WO,   "Resets the alarm log"                                     ),
    Dataitem("AUTOMATIC",                          3,  52, ACC_WO,   "Sets the pump in Control Mode Automatic"                  ),
    Dataitem("TWIN_MODE_SPARE",                    3,  58, ACC_WO,   "Twin Pump Mode Spare"                                     ),
    Dataitem("TWIN_MODE_ALT",                      3,  59, ACC_WO,   "Twin Pump Mode Alternating"                               ),
    Dataitem("TWIN_MODE_SYNC",                     3,  60, ACC_WO,   "Twin Pump Mode Syncrouneous"                              ),
    Dataitem("NIGHT_REDUCT_E+",                    3,  66, ACC_WO,   "Enables Night Reduction"                                  ),
    Dataitem("NIGHT_REDUCT_D+",                    3,  67, ACC_WO,   "Disables Night Reduction"                                 ),

    Dataitem("unit_addr",                          4,  46, ACC_WR,   "GENIbus/GENIlink unit address"                            ),
    Dataitem("group_addr",                         4,  47, ACC_WR,   "GENIbus group address"                                    ),
    Dataitem("min_curve_no",                       4,  74, ACC_WR,   "Minimum curve No."                                        ),
    Dataitem("h_const_ref_min",                    4,  83, ACC_WR,   "Constant Pressure Mode minimum reference"                 ),
    Dataitem("h_const_ref_max",                    4,  84, ACC_WR,   "Constant Pressure Mode maximum reference"                 ),
    Dataitem("h_prop_ref_min",                     4,  85, ACC_WR,   "Proportional Pressure Mode minimum reference"             ),
    Dataitem("h_prop_ref_max",                     4,  86, ACC_WR,   "Proportional Pressure Mode maximum reference"             ),
    Dataitem("ref_steps",                          4,  87, ACC_WR,   "No. of discrete reference steps"                          ),

    Dataitem("ref_rem",                            5,   1, ACC_WO,   "GENIbus setpoint (Remote reference)"                      ),
    Dataitem("ref_ir",                             5,   2, ACC_WO,   "GENIlink setpoint (curve No.)"                            ),
    Dataitem("ref_att_rem",                        5,  19, ACC_WO,   "Remote reference attenuation"                             ),

    Dataitem("product_name",                       7,   1, ACC_RO,   ""                                                         ),
    Dataitem("software_name1",                     7,   3, ACC_RO,   ""                                                         ),
    Dataitem("compile_date1",                      7,   4, ACC_RO,   ""                                                         ),
    Dataitem("protocol_code",                      7,   5, ACC_RO,   ""                                                         ),
    Dataitem("developers",                         7,   7, ACC_RO,   ""                                                         ),
    Dataitem("rtos_code",                          7,  12, ACC_RO,   ""                                                         ),
)


def addToDict(d, k, v):
    d[k] = v


COMMANDS = dict()
MEASUREMENT_VALUES = dict()
REFERENCES = dict()
PARAMETER = dict()
STRINGS = dict()


for item in DATAITEMS:
    if item.klass == 2:
        addToDict(MEASUREMENT_VALUES, item.name, item)
    elif item.klass == 3:
        addToDict(COMMANDS, item.name, item)
    elif item.klass == 4:
        addToDict(PARAMETER, item.name, item)
    elif item.klass == 5:
        addToDict(REFERENCES, item.name, item)
    elif item.klass == 7:
        addToDict(STRINGS, item.name, item)


#print MEASUREMENT_VALUES
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
