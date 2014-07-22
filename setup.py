#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Radim Rehurek <radimrehurek@seznam.cz>

"""
Run with:

sudo python ./setup.py install
"""

import os

from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = 'sqlitedict',
    version = '1.2.0',
    description = 'Persistent dict in Python, backed up by sqlite3 and pickle, multithread-safe.',
    long_description = read('README.rst'),

    py_modules = ['sqlitedict'],

    # there is a bug in python2.5, preventing distutils from using any non-ascii characters :( http://bugs.python.org/issue2562
    author = 'Radim Rehurek, Victor R: Escobar', # u'Radim Řehůřek, Víctor R. Escobar' <-- missing encoding support
    author_email = 'radimrehurek@seznam.cz, victor.r.e.o@gmail.com',
    url = 'https://github.com/piskvorky/sqlitedict',
    download_url = 'http://pypi.python.org/pypi/sqlitedict',

    keywords = 'sqlite, persistent dict, multithreaded',

    license = 'public domain',
    platforms = 'any',

    classifiers = [ # from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5', # I wonder if there is a shortcut for that
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2.8',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Database :: Front-Ends',
    ],

)
