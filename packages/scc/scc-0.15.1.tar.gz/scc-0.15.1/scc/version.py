#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2014 University of Dundee & Open Microscopy Environment
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


from __future__ import print_function
import yaclifw.version
from pkg_resources import resource_string


class Version(yaclifw.version.Version):
    """Find which version of this library is being used"""

    FILE = __file__

    def __call__(self, args):
        super(yaclifw.version.Version, self).__call__(args)
        v = resource_string(__name__, 'RELEASE-VERSION')
        v = v.rstrip().decode('utf-8')
        print(v)
