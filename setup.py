#!/bin/env/python
# -*- coding: utf-8 -*-

from distutils.core import setup, Extension
from glob import glob
from setuptools import find_packages
import sys

VER = sys.version_info.major, sys.version_info.minor

if VER < (3, 4):
    REQS = ['PyQt5', 'mako', 'pyserial', 'enum']	# 'enum' backport needed.
else:
    REQS = ['PyQt5', 'mako', 'pyserial']

setup(
    name = 'genibus',
    version = '0.1',
    description= "GENIBus library",
    author = 'Christoph Schueler',
    author_email = 'cpu12.gems@googlemail.com',
    url = 'https://github.com/christoph2/GENIBus-Arduino',
    packages = ['genibus', 'genibus/devices', 'genibus/linklayer', 'genibus/datamanager', 'genibus/framing', 'genibus/utils'],
#    entry_points = {
#        'console_scripts': [
#                'GeniControl = genicontrol.GeniControl:main',
#        ],
#    },
    install_requires = REQS,
    data_files = [
            ('genibus/config', glob('genibus/config/*.json')), 
            ('genibus/devices', glob('genibus/devices/*.json')),
    ],
    test_suite="tests"
)
