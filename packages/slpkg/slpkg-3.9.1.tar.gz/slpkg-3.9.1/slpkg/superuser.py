#!/usr/bin/python3
# -*- coding: utf-8 -*-

# superuser.py file is part of slpkg.

# Copyright 2014-2021 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# Slpkg is a user-friendly package manager for Slackware installations

# https://gitlab.com/dslackw/slpkg

# Slpkg is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import getpass


def s_user():
    """Check for root user
    """
    if getpass.getuser() != "root":
        print("\nslpkg: Error: Must have root privileges\n")
        raise SystemExit(1)
