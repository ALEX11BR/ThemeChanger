# Copyright (C) 2021  Popa Ioan Alexandru
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

from shutil import get_unpack_formats

from gi.repository import Gtk

class ArchiveFileFilter(Gtk.FileFilter):
    def __init__(self):
        super().__init__()

        self.set_name("Supported archive formats")

        for formatTuple in get_unpack_formats():
            for supportedFormat in formatTuple[1]:
                self.add_pattern("*" + supportedFormat)