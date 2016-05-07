#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This code is distributed under the terms and conditions
# from the Apache License, Version 2.0
#
# http://opensource.org/licenses/apache2.0.php

"""
Run with:

python ./setup.py install
"""

import os
import io
import subprocess

import setuptools.command.develop
from distutils.core import setup


def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    return io.open(path, encoding='utf8').read()


class SetupDevelop(setuptools.command.develop.develop):
    """Docstring is overwritten."""

    def run(self):
        """
        Prepare environment for development.

        - Ensures 'nose' and 'coverage.py' are installed for testing.
        - Call super()'s run method.
        """
        subprocess.check_call(('pip', 'install', 'nose', 'coverage'))

        # Call super() (except develop is an old-style class, so we must call
        # directly). The effect is that the development egg-link is installed.
        setuptools.command.develop.develop.run(self)

SetupDevelop.__doc__ = setuptools.command.develop.develop.__doc__


setup(
    name='sqlitedict',
    version='1.4.1',
    description='Persistent dict in Python, backed up by sqlite3 and pickle, multithread-safe.',
    long_description=read('README.rst'),

    py_modules=['sqlitedict'],

    # there is a bug in python2.5, preventing distutils from using any non-ascii characters :(
    # http://bugs.python.org/issue2562
    author='Radim Rehurek, Victor R. Escobar, Andrey Usov, Prasanna Swaminathan, Jeff Quast',
    author_email="various",
    maintainer='Radim Rehurek',
    maintainer_email='me@radimrehurek.com',

    url='https://github.com/piskvorky/sqlitedict',
    download_url='http://pypi.python.org/pypi/sqlitedict',

    keywords='sqlite, persistent dict, multithreaded',

    license='Apache 2.0',
    platforms='any',

    classifiers=[  # from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Database :: Front-Ends',
    ],
    cmdclass={'develop': SetupDevelop},
)
