unsigned char InfoRequest0[] = {
    0x27,
    0x13,
    0x20,
    0x04,

    0x02,  /* Class 2 - Measurered Data */
    0xcf,
    0xa6,  /* Twin Pump Mode, UPED's only */
    0x59,  /* Logical value of all external control inputs */
    0x42,  /* Quick Shut Down Alarm No. 1 */
    0x43,  /* Quick Shut Down Alarm No. 2 */
    0x4d,  /* Stop Alarm No. 1 backup */
    0x9e,  /* Actual alarm */
    0x61,  /* Selected curve No. (LED bar indicator No.) */
    0x4e,  /* Stop Alarm No. 2 backup */
    0x4b,  /* Quick Shut Down Alarm No. 1 backup */
    0x23,  /* Pump speed */
    0x29,  /* Maximum power consumption */
    0x47,  /* Survive Alarm No. 2 */
    0x4a,  /* Start Alarm No. 2 backup */
    0xa2,  /* Logged alarm code No. 4 */
    0x5a,  /* Currently active contr. source and priority */

    0xef,
    0xe4,

};

unsigned char InfoRequest1[] = {
    0x27,
    0x13,
    0x20,
    0x04,

    0x02,  /* Class 2 - Measurered Data */
    0xcf,
    0x1d,  /* Temp. in motor or in frequency converter module */
    0x1e,  /* Motor current */
    0x1f,  /* Mains supply current */
    0x94,  /* Unit family code */
    0x98,  /* Accumulated electric energy consumption */
    0x46,  /* Survive Alarm No. 1 */
    0x1c,  /* Temperature in contdefs.ACC_ROl electdefs.ACC_ROnics */
    0x95,  /* Unit type code */
    0x99,  /* Accumulated electric energy consumption */
    0x3d,  /* Local reference attenuator input */
    0x49,  /* Start Alarm No. 1 backup */
    0x1b,  /* Frequency converter DC link voltage */
    0x25,  /* Actual pump head */
    0x41,  /* Start Alarm No. 2 */
    0x40,  /* Start Alarm No. 1 */

    0x2d,
    0x19,

};

unsigned char InfoRequest2[] = {
    0x27,
    0x13,
    0x20,
    0x04,

    0x02,  /* Class 2 - Measurered Data */
    0xcf,
    0x3a,  /* Water temperature */
    0x4c,  /* Quick Shut Down Alarm No. 2 backup */
    0xa0,  /* Logged alarm code No. 2 */
    0xa1,  /* Logged alarm code No. 3 */
    0x20,  /* Actual control signal (freq. or voltage) applied to pump */
    0x57,  /* Remote setup */
    0x48,  /* Indication Alarm */
    0x2c,  /* Maximum pump head (closed valve) */
    0xa3,  /* Logged alarm code No. 5 */
    0x93,  /* Control loop reference */
    0x4f,  /* Survive Alarm No.1 backup */
    0x3e,  /* Selected system control loop reference */
    0x44,  /* Stop Alarm No. 1 */
    0x30,  /* Actual reference */
    0x5d,  /* Stop Alarm No. 3 */

    0x4f,
    0x2a,

};

unsigned char InfoRequest3[] = {
    0x27,
    0x13,
    0x20,
    0x04,

    0x02,  /* Class 2 - Measurered Data */
    0xcf,
    0x2b,  /* Maximum possible flow at maximum power consum. */
    0x60,  /* Stop Alarm No. 3 backup */
    0x31,  /* Reference influence */
    0x2e,  /* Back up byte to indication alarm */
    0x53,  /* Actual Mode Status No. 3 */
    0x52,  /* Actual Mode Status No. 2 */
    0x51,  /* Actual Mode Status No. 1 */
    0x9b,  /* Interpreted (filtered) version of alarm_code */
    0x96,  /* Unit version code */
    0x50,  /* Survive Alarm No.2 backup */
    0x55,  /* Local setup */
    0x2f,  /* Status of green and red indication diodes */
    0x27,  /* Actual pump flow */
    0x22,  /* Power consumption */
    0x45,  /* Stop Alarm No. 2 */

    0xdc,
    0x19,

};

unsigned char InfoRequest4[] = {
    0x27,
    0x0a,
    0x20,
    0x04,

    0x02,  /* Class 2 - Measurered Data */
    0xc6,
    0x19,  /* Two hour counter */
    0x9f,  /* Logged alarm code No. 1 */
    0x28,  /* Local reference setting */
    0x1a,  /* Frequency converter DC link current */
    0x2a,  /* Minimum possible flow at maximum power consum. */
    0x18,  /* Two hour counter */

    0x89,
    0x97,

};

unsigned char InfoRequest5[] = {
    0x27,
    0x0c,
    0x20,
    0x04,

    0x04,  /* Class 4 - Configuration Parameters */
    0xc8,
    0x4a,  /* Minimum curve No. */
    0x55,  /* Proportional Pressure Mode minimum reference */
    0x2f,  /* GENIbus group address */
    0x56,  /* Proportional Pressure Mode maximum reference */
    0x2e,  /* GENIbus/GENIlink unit address */
    0x54,  /* Constant Pressure Mode maximum reference */
    0x53,  /* Constant Pressure Mode minimum reference */
    0x57,  /* No. of discrete reference steps */

    0x38,
    0x86,

};

unsigned char InfoRequest6[] = {
    0x27,
    0x07,
    0x20,
    0x04,

    0x05,  /* Class 5 - Reference Values */
    0xc3,
    0x01,  /* GENIbus setpoint (Remote reference) */
    0x13,  /* Remote reference attenuation */
    0x02,  /* GENIlink setpoint (curve No.) */

    0x2b,
    0xf3,

};

