#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2012 University of Dundee & Open Microscopy Environment
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
SCC distribution script
"""

from setuptools import setup

from setuptools.command.test import test as TestCommand
import os
import sys


class PyTest(TestCommand):
    user_options = [
        ('test-path=', 't', "base dir for test collection"),
        ('test-pythonpath=', 'p', "prepend 'pythonpath' to PYTHONPATH"),
        ('test-string=', 'k', "only run tests including 'string'"),
        ('test-marker=', 'm', "only run tests including 'marker'"),
        ('test-no-capture', 's', "don't suppress test output"),
        ('test-failfast', 'x', "Exit on first error"),
        ('test-verbose', 'v', "more verbose output"),
        ('test-quiet', 'q', "less verbose output"),
        ('junitxml=', None, "create junit-xml style report file at 'path'"),
        ('pdb', None, "fallback to pdb on error"),
        ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.test_pythonpath = None
        self.test_string = None
        self.test_marker = None
        self.test_path = 'test'
        self.test_failfast = False
        self.test_quiet = False
        self.test_verbose = False
        self.test_no_capture = False
        self.junitxml = None
        self.pdb = False

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [self.test_path]
        if self.test_string is not None:
            self.test_args.extend(['-k', self.test_string])
        if self.test_marker is not None:
            self.test_args.extend(['-m', self.test_marker])
        if self.test_failfast:
            self.test_args.extend(['-x'])
        if self.test_verbose:
            self.test_args.extend(['-v'])
        if self.test_quiet:
            self.test_args.extend(['-q'])
        if self.test_no_capture:
            self.test_args.extend(['-s'])
        if self.junitxml is not None:
            self.test_args.extend(['--junitxml', self.junitxml])
        if self.pdb:
            self.test_args.extend(['--pdb'])
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


with open(os.path.join('scc', 'RELEASE-VERSION')) as version_file:
    VERSION = version_file.read().strip()

LONG_DESCRIPTION = open("README.rst", "r").read()

CLASSIFIERS = ["Development Status :: 4 - Beta",
               "Environment :: Console",
               "Intended Audience :: Developers",
               "License :: OSI Approved :: GNU General Public License v2"
               " (GPLv2)",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Software Development :: Version Control"]

setup(name='scc',

      # Simple strings
      author='The Open Microscopy Team',
      author_email='ome-devel@lists.openmicroscopy.org.uk',
      description='OME tools for managing the git(hub) workflow',
      license='GPLv2',
      url='https://github.com/ome/scc',

      # More complex variables
      packages=['scc'],
      include_package_data=True,
      install_requires=['yaclifw>=0.2.0,<0.3',
                        'PyGithub>=1.54',
                        'argparse',
                        'future',
                        'PyYAML>=5.1',
                        'six'],
      entry_points={'console_scripts': ['scc = scc.main:entry_point']},
      zip_safe=True,

      # Using global variables
      long_description=LONG_DESCRIPTION,
      classifiers=CLASSIFIERS,
      version=VERSION,
      python_requires=">=3.5",
      cmdclass={'test': PyTest},
      tests_require=[
          'pytest<3.3',
          'restview',
          'mox3'
      ],
      )
