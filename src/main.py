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

import os
import sys

from gi.repository import Gtk, Gio, GLib

from .window import ThemechangerWindow

class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.github.alex11br.themechanger',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = ThemechangerWindow(app=self)
        win.present()


def main(version):
    # Here we're making some dirs necessary to prevent some "file not found" errors when saving
    os.makedirs(os.path.join(GLib.get_user_config_dir(), "gtk-3.0"), exist_ok=True)
    os.makedirs(os.path.join(GLib.get_user_config_dir(), "gtk-4.0"), exist_ok=True)
    os.makedirs(os.path.join(GLib.get_user_config_dir(), "Kvantum"), exist_ok=True)
    os.makedirs(os.path.join(GLib.get_home_dir(), ".icons", "default"), exist_ok=True)
    # Here we're good guys and touch the xsettingsd config file, as xsettingsd won't run at all if there's no config file
    os.makedirs(os.path.join(GLib.get_user_config_dir(), "xsettingsd"), exist_ok=True)
    open(os.path.join(GLib.get_user_config_dir(), "xsettingsd", "xsettingsd.conf"), "a").close()

    app = Application()
    return app.run(sys.argv)
