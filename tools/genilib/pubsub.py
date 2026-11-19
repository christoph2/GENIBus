#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
## Minimal replacement for the old ``wx.lib.pubsub`` "arg1" protocol,
## which was removed in wxPython 4.
##
## Supported API (as used by GeniControl):
##   pub.subscribe(listener, topic)
##   pub.unsubscribe(listener, topic)
##   pub.sendMessage(topic, data=None)
##
## Topics are dotted strings ("Measurements.speed_hi") or tuples.  Listeners
## subscribed to a parent topic ("Measurements") also receive messages sent
## to its sub-topics.  Listeners get one argument, a ``Message`` object with
## ``.topic`` (tuple of topic parts) and ``.data``.
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##

import threading


class Message(object):

    def __init__(self, topic, data=None):
        self.topic = topic
        self.data = data

    def __repr__(self):
        return "Message(topic=%r, data=%r)" % (self.topic, self.data)


def _normalize(topic):
    if isinstance(topic, (tuple, list)):
        return tuple(topic)
    return tuple(str(topic).split('.'))


class Publisher(object):

    def __init__(self):
        self._lock = threading.RLock()
        self._listeners = {}

    def subscribe(self, listener, topic):
        topic = _normalize(topic)
        with self._lock:
            listeners = self._listeners.setdefault(topic, [])
            if listener not in listeners:
                listeners.append(listener)

    def unsubscribe(self, listener, topic=None):
        with self._lock:
            topics = [_normalize(topic)] if topic is not None else list(self._listeners.keys())
            for t in topics:
                listeners = self._listeners.get(t, [])
                if listener in listeners:
                    listeners.remove(listener)

    def unsubAll(self):
        with self._lock:
            self._listeners.clear()

    def sendMessage(self, topic, data=None):
        topic = _normalize(topic)
        message = Message(topic, data)
        with self._lock:
            receivers = []
            # Exact topic and all parent topics.
            for idx in range(len(topic), 0, -1):
                receivers.extend(self._listeners.get(topic[:idx], []))
        for listener in receivers:
            listener(message)


pub = Publisher()
