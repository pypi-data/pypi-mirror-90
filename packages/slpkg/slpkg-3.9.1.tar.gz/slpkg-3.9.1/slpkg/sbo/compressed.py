#!/usr/bin/python3
# -*- coding: utf-8 -*-

# download.py file is part of slpkg.

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


class SBoLink:
    """Create slackbuild tar.gz archive from url
    """
    def __init__(self, sbo_url):
        self.sbo_url = sbo_url

    def tar_gz(self):
        """Return link slackbuild tar.gz archive
        """
        return f"{self.sbo_url[:-1]}.tar.gz"
