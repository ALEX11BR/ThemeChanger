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
import subprocess

from gi.repository import GLib

class BaseApplyThemes:
    def applyThemes(self, props, gtk2Theme, gtk4Theme, kvantumTheme, cssText):
        gtkKeyFile = GLib.KeyFile()

        gtkKeyFile.set_string("Settings", "gtk-theme-name", gtk4Theme)
        gtkKeyFile.set_boolean("Settings", "gtk-application-prefer-dark-theme", props.gtk_application_prefer_dark_theme)
        gtkKeyFile.set_string("Settings", "gtk-icon-theme-name", props.gtk_icon_theme_name)
        if props.gtk_cursor_theme_name:
            gtkKeyFile.set_string("Settings", "gtk-cursor-theme-name", props.gtk_cursor_theme_name)
        gtkKeyFile.set_integer("Settings", "gtk-cursor-theme-size", props.gtk_cursor_theme_size)
        gtkKeyFile.set_string("Settings", "gtk-font-name", props.gtk_font_name)
        gtkKeyFile.set_integer("Settings", "gtk-xft-antialias", props.gtk_xft_antialias)
        gtkKeyFile.set_integer("Settings", "gtk-xft-hinting", props.gtk_xft_hinting)
        gtkKeyFile.set_string("Settings", "gtk-xft-hintstyle", props.gtk_xft_hintstyle or "hintnone")
        gtkKeyFile.set_string("Settings", "gtk-xft-rgba", props.gtk_xft_rgba or "none")
        gtkKeyFile.set_integer("Settings", "gtk-xft-dpi", props.gtk_xft_dpi)
        gtkKeyFile.set_boolean("Settings", "gtk-overlay-scrolling", props.gtk_overlay_scrolling)

        gtkKeyFile.save_to_file(os.path.join(GLib.get_user_config_dir(), "gtk-4.0", "settings.ini"))

        gtkKeyFile.set_string("Settings", "gtk-theme-name", props.gtk_theme_name)
        if props.gtk_key_theme_name:
            gtkKeyFile.set_string("Settings", "gtk-key-theme-name", props.gtk_key_theme_name)
        gtkKeyFile.set_boolean("Settings", "gtk-menu-images", props.gtk_menu_images)
        gtkKeyFile.set_boolean("Settings", "gtk-button-images", props.gtk_button_images)

        gtkKeyFile.save_to_file(os.path.join(GLib.get_user_config_dir(), "gtk-3.0", "settings.ini"))

        if props.gtk_cursor_theme_name:
            iconKeyFile = GLib.KeyFile()
            iconKeyFile.set_string("Icon Theme", "Name", "Default")
            iconKeyFile.set_string("Icon Theme", "Comment", "Default icon theme")
            iconKeyFile.set_string("Icon Theme", "Inherits", props.gtk_cursor_theme_name)
            iconKeyFile.save_to_file(os.path.join(GLib.get_home_dir(), ".icons", "default", "index.theme"))
            
        if kvantumTheme:
            kvantumKeyFile = GLib.KeyFile()
            kvantumKeyFile.set_string("General", "theme", kvantumTheme)
            kvantumKeyFile.save_to_file(os.path.join(GLib.get_user_config_dir(), "Kvantum", "kvantum.kvconfig"))
        
        with open(os.path.join(GLib.get_home_dir(), ".gtkrc-2.0"), "w") as gtk2File:
            gtk2File.write(f'gtk-theme-name="{gtk2Theme}"\n')
            gtk2File.write(f'gtk-icon-theme-name="{props.gtk_icon_theme_name}"\n')
            if props.gtk_cursor_theme_name:
                gtk2File.write(f'gtk-cursor-theme-name="{props.gtk_cursor_theme_name}"\n')
            gtk2File.write(f'gtk-font-name="{props.gtk_font_name}"\n')
            gtk2File.write(f'gtk-menu-images={int(props.gtk_menu_images)}\n')
            gtk2File.write(f'gtk-cursor-theme-size={props.gtk_cursor_theme_size}\n')
            gtk2File.write(f'gtk-button-images={int(props.gtk_button_images)}\n')
            gtk2File.write(f'gtk-xft-antialias={props.gtk_xft_antialias}\n')
            gtk2File.write(f'gtk-xft-hinting={props.gtk_xft_hinting}\n')
            gtk2File.write(f'gtk-xft-hintstyle="{props.gtk_xft_hintstyle}"\n')
            gtk2File.write(f'gtk-xft-rgba="{props.gtk_xft_rgba}"\n')
            gtk2File.write(f'gtk-xft-dpi={props.gtk_xft_dpi}\n')

        with open(os.path.join(GLib.get_user_config_dir(), "gtk-3.0", "gtk.css"), "w") as cssFile:
            cssFile.write(cssText)
        with open(os.path.join(GLib.get_user_config_dir(), "gtk-4.0", "gtk.css"), "w") as cssFile:
            cssFile.write(cssText)

        
class XsettingsdApplyThemes(BaseApplyThemes):
    def __init__(self):
        self.confFolder = os.path.join(GLib.get_user_config_dir(), "xsettingsd")
        try:
            os.mkdir(self.confFolder)
        except:
            pass
        self.confFile = os.path.join(self.confFolder, "xsettingsd.conf")

    def applyThemes(self, props, **kwargs):
        super().applyThemes(props, **kwargs)

        options = {
            "Net/ThemeName": f'"{props.gtk_theme_name}"',
            "Net/IconThemeName": f'"{props.gtk_icon_theme_name}"',
            "Xft/Antialias": props.gtk_xft_antialias,
            "Xft/Hinting": props.gtk_xft_hinting,
            "Xft/HintStyle": f'"{props.gtk_xft_hintstyle or "hintnone"}"',
            "Xft/RGBA": f'"{props.gtk_xft_rgba or "none"}"',
            "Xft/DPI": props.gtk_xft_dpi,
            "Gtk/CursorThemeName": f'"{props.gtk_cursor_theme_name or "default"}"',
            "Gtk/FontName": f'"{props.gtk_font_name}"',
            "Gtk/KeyThemeName": f'"{props.gtk_key_theme_name or ""}"',
            "Gtk/MenuImages": int(props.gtk_menu_images),
            "Gtk/ButtonImages": int(props.gtk_button_images),
        }

        with open(self.confFile, "w") as file:
            for option in options:
                file.write(f'{option} {options[option]}\n')
        
        subprocess.run(["pkill", "-HUP", "^xsettingsd$"])

def getThemeApplier():
    if subprocess.call(["pidof", "xsettingsd"], stdout=subprocess.DEVNULL) == 0:
        return XsettingsdApplyThemes()
    else:
        return BaseApplyThemes()
