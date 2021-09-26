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

import fileinput
import os
import subprocess

from gi.repository import GLib

class DummyApplyThemes:
    def applyThemes(self, **kwargs):
        print("Can't instantaneously apply themes")

class XsettingsdApplyThemes(DummyApplyThemes):
    def __init__(self):
        self.confFolder = os.path.join(GLib.get_user_config_dir(), "xsettingsd")
        try:
            os.mkdir(self.confFolder)
        except:
            pass

    def applyThemes(self, **kwargs):
        options = {
            "Net/ThemeName": f'"{kwargs["gtkTheme"]}"',
            "Net/IconThemeName": f'"{kwargs["iconTheme"]}"',
            "Xft/Antialias": kwargs["antialias"],
            "Xft/Hinting": kwargs["hinting"],
            "Xft/HintStyle": f'"{kwargs["hintstyle"]}"',
            "Xft/RGBA": f'"{kwargs["rgba"]}"',
            "Xft/DPI": kwargs["dpi"],
            "Gtk/CursorThemeName": f'"{kwargs["cursorTheme"]}"',
            "Gtk/FontName": f'"{kwargs["fontName"]}"',
            "Gtk/KeyThemeName": f'"{kwargs["keyTheme"]}"',
            "Gtk/MenuImages": int(kwargs["menuImages"]),
            "Gtk/ButtonImages": int(kwargs["buttonImages"]),
        }

        confFile = os.path.join(self.confFolder, "xsettingsd.conf")
        #for line in fileinput.FileInput(confFile, inplace=True):
        #    if not line.split()[0] in options:
        #        print(line, end="")
            
        with open(confFile, "w") as file:
            for option in options:
                file.write(f'{option} {options[option]}\n')
        
        subprocess.run(["pkill", "-HUP", "^xsettingsd$"])

def getThemeApplier():
    if subprocess.call(["pidof", "xsettingsd"], stdout=subprocess.DEVNULL) == 0:
        return XsettingsdApplyThemes()
    else:
        return DummyApplyThemes()