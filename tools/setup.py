#!/bin/env/python

from distutils.core import setup,Extension
from glob import glob
from setuptools import find_packages

print find_packages()

setup(
    name = 'genicontrol',
    version = '0.1',
    description= "GENIBus library",
    author = 'Christoph Schueler',
    author_email = 'cpu12.gems@googlemail.com',
    url = 'https://github.com/christoph2/GENIBus-Arduino',
    packages = ['genicontrol', 'genicontrol/model', 'genicontrol/view', 'genicontrol/controller', 'genilib', 'genilib/utils'],
    entry_points = {
	'console_scripts': [
		'GeniControl = genicontrol.GeniControl:main',
        ],
    },
    install_requires = ['mako', 'pyserial', 'pyyaml'],
    data_files = [
            ('genicontrol/config', glob('genicontrol/config/*.*')),
    ]
)
