#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
##
## Grundfos GENIBus Library for Arduino.
##
## (C) 2007-2013 by Christoph Schueler <github.com/Christoph2,
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

import logging
import threading
import time
import Queue

class PendingRequestError(Exception): pass
class RequestTimeoutError(Exception): pass


class WorkerThread(threading.Thread):
    logger = logging.getLogger("genicontrol")

    def __init__(self, req, resp, respEvent, cancelEvent):
        super(WorkerThread, self).__init__()
        self._request = req
        self._response = resp
        self._respEvent = respEvent
        self._cancelEvent = cancelEvent

    def run(self):
        name = self.getName()
        print "Starting %s." % name
        #while True:
        #    if self._cancelEvent.isSet():
        #        break
        #    time.sleep(0.1)
        #self._respEvent.set()
        self._cancelEvent.wait(5.0)
        print "Exiting %s." % name


class RequestorThread(threading.Thread):
    def __init__(self):
        super(RequestorThread, self).__init__()

    def run(self):
        pass


class Requestor(object):
    IDLE    = 0
    PENDING = 1
    TIMEOUT = 2
    _clsLock = threading.Lock()
    _requLock = threading.Lock()
    _respEvent = threading.Event()
    _cancelEvent = threading.Event()
    _currentRequest = None
    _currentResponse = None
    logger = logging.getLogger("genicontrol")

    def __new__(cls):
        try:
            cls._clsLock.acquire()
            if not hasattr(cls, '_instance'):
                cls._state = cls.IDLE
                cls._instance = super(cls.__class__, cls).__new__(cls)
        finally:
            cls._clsLock.release()
        return cls._instance

    def request(self, req):
        if Requestor._state == Requestor.PENDING:
            ## Concurrent requests are not supported by GENIBus.
            raise PendingRequestError('There is already a pending request.')
        try:
            Requestor._requLock.acquire()
            Requestor._state = Requestor.PENDING
            Requestor._currentRequest = req
            worker = WorkerThread(req, Requestor._currentResponse, Requestor._respEvent, Requestor._cancelEvent)
            worker.run()
            if not Requestor._respEvent.wait(1.0):
                print "Cancelling %s." % worker.getName()
                Requestor._cancelEvent.set()
                worker.join()
                raise RequestTimeoutError("Request timed out.")
            else:
                pass # TODO: process/dissect response.
        except Exception as e:
            print str(e)
        finally:
            Requestor._requLock.release()


def buildLPDU():
    pass


def main():
    req = Requestor()
    req.request([])

if __name__ == '__main__':
    main()

