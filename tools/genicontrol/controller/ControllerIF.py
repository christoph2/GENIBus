#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
from wx.lib.pubsub import Publisher as Publisher

DATA_NOT_AVAILABLE = 0xff

class IController(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, model, viewClass):
        self._pub = Publisher()
        self._model = model
        self._view = viewClass(self, model)
        # TODO: Create and disable controls.
        self._model.initialize()


