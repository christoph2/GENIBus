#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import genicontrol.dataitems as dataitems
from genicontrol.simu.Simulator import DATA_POOL

class TestDataPool(unittest.TestCase):
    def testCorrectnessOfKeys(self):
        for klass, values in DATA_POOL.items():
            di = dataitems.DATAITEMS_FOR_CLASS[klass]
            for value in values:
                if not value.name in di:
                    raise KeyError('invalid datapoint "%s"' % value.name)

def main():
    unittest.main()

if __name__ == '__main__':
    main()

