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

    def __init__(self, req, resp, respQueue, cancelEvent):
        super(WorkerThread, self).__init__()
        self._request = req
        self._response = resp
        self._respQueue = respQueue
        self._cancelEvent = cancelEvent

    def run(self):
        name = self.getName()
        print "Starting %s." % name
        while True:
            if self._cancelEvent.isSet():
                break
            time.sleep(0.1)
        self._respQueue.put([])
        self._cancelEvent.wait(2.0)
        print "Exiting %s." % name


class RequestorThread(threading.Thread):
    IDLE    = 0
    PENDING = 1
    TIMEOUT = 2
    _clsLock = threading.Lock()
    _respQueue = Queue.Queue()
    _cancelEvent = threading.Event()
    _currentRequest = None
    _currentResponse = None
    logger = logging.getLogger("genicontrol")

    def __new__(cls, *args):
        try:
            cls._clsLock.acquire()
            if not hasattr(cls, '_instance'):
                cls._state = cls.IDLE
                cls._instance = super(cls.__class__, cls).__new__(cls)
        finally:
            cls._clsLock.release()
        return cls._instance


    def __init__(self, evt):
        super(RequestorThread, self).__init__()
        self.evt = evt

    def run(self):
        while True:
            res = self.evt.wait(1.0)
            if res:
                print "Exiting RequestorThread"
                RequestorThread._cancelEvent.set()
                self.worker.join()
                break
            print "Running requestorThread."
            if RequestorThread._state == Requestor.IDLE:
                self.request([])

    def request(self, req):
        RequestorThread._state = Requestor.PENDING
        RequestorThread._currentRequest = req
        self.worker = WorkerThread(req, RequestorThread._currentResponse, RequestorThread._respQueue, RequestorThread._cancelEvent)
        self.worker.start()
        success = True
        try:
            response = RequestorThread._respQueue.get(True, 2.0)
        except Queue.Empty:
            success = False
        if not success:
            print "Cancelling %s." % self.worker.getName()
            RequestorThread._cancelEvent.set()
            self.worker.join()
            RequestorThread._cancelEvent.clear()
        else:
            print "Processing Response."
        RequestorThread._state = Requestor.IDLE

def buildLPDU():
    pass


def main():
    fin  = threading.Event()
    req = RequestorThread(fin)
    req.start()
    time.sleep(10)
    fin.set()
    req.join()

if __name__ == '__main__':
    main()

"""
def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()

q = Queue()
for i in range(num_worker_threads):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

for item in source():
    q.put(item)

q.join()
"""

