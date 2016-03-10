/*
 *  Grundfos GENIBus Library.
 *
 * (C) 2007-2016 by Christoph Schueler <github.com/Christoph2,
 *                                      cpu12.gems@googlemail.com>
 *
 * All Rights Reserved
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 *
 */

#include <string.h>
#include <stdint.h>
#include <stdio.h>
#include <unistd.h>
#include <error.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <sys/time.h>
#include <sys/types.h>
#include <time.h>
#include <signal.h>
#include <fcntl.h>


#include "genibus/posix_timer.h"

#define TIMER_SIGNAL    SIGUSR1

void Win_Error(char * function, uint32_t err);

void timerTest(void);
void TimerISR(int sig, siginfo_t * extra, void * cruft);
void Port_Timer_Start(long millis);

static timer_t timerid;
static Port_Timer_ConfigType const * timerConfiguration = NULL;
extern Port_Timer_ConfigType Port_Timer_Configuration;

sig_atomic_t myISRVar = 0;

void TimerISR(int sig, siginfo_t * extra, void * cruft)
{
    //int count;
    if (sig == TIMER_SIGNAL) {
/*
        for (count = 0; count < (1 + timer_getoverrun(timerid)); ++count) {
            timerConfiguration->tickHandler();
        }
*/
        timerConfiguration->tickHandler();
    } else {
        printf("Other signal [%u]\n", sig);
    }
}

void Port_Timer_Init(Port_Timer_ConfigType const * const config)
{
    struct sigevent evp;
    struct sigaction sa;

    timerConfiguration = config;

    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_SIGINFO;
    sa.sa_sigaction = TimerISR;
    if(sigaction(TIMER_SIGNAL, &sa, NULL) < 0)
    {
        Win_Error("sigaction", errno);
    }

    memset(&evp, 0, sizeof (struct sigevent));
    evp.sigev_notify = SIGEV_SIGNAL;
    evp.sigev_signo = TIMER_SIGNAL;

    timer_create(CLOCK_REALTIME, &evp, &timerid);
}


void Port_Timer_Deinit(void)
{
    if (timer_delete(timerid) == -1) {
        Win_Error("timer_delete", errno);
    }
}

void Port_Timer_Start(long millis)
{
    struct itimerspec value;

    value.it_interval.tv_sec = 0;
    value.it_interval.tv_nsec = 1000 * millis;
    value.it_value.tv_sec = 0;
    value.it_value.tv_nsec = 1000 * millis;

    if (timer_settime(timerid, 0, &value, NULL) == -1) {
        Win_Error("timer_settime", errno);
    }
}

void Port_Timer_Stop(void)
{
    struct itimerspec value;

    value.it_interval.tv_sec = 0;
    value.it_interval.tv_nsec = 0;
    value.it_value.tv_sec = 0;
    value.it_value.tv_nsec = 0;

    if (timer_settime(timerid, 0, &value, NULL) == -1) {
        Win_Error("timer_settime", errno);
    }
}


#if 0
clock_t start, end;
double cpu_time_used;

start = clock();
… /* Do the work. */
end = clock();
cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
#endif


void timerTest(void)
{
    int i;
    Port_Timer_Init(&Port_Timer_Configuration);
    Port_Timer_Start(timerConfiguration->tickResolution);
/*
    for (i = 0; i < 10; ++i) {
        sleep(1);
        //nanosleep();
    }
*/
    //Port_Timer_Deinit();
}

