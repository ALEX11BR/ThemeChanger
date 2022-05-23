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

from gi.repository import GLib, Gio

class BaseApplyThemes:
    """
    The base theme applying mechanism: write themes and settings to config files
    """
    def applyThemes(self, props, gtk2Theme, gtk4Theme, kvantumTheme, kvantumThemeFilePath, cssText):
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
            kvantumThemeKeyFile = GLib.KeyFile()
            if kvantumThemeFilePath[:2] != "//":
                kvantumThemeKeyFile.load_from_file(kvantumThemeFilePath, GLib.KeyFileFlags.NONE)
            else:
                kvantumThemeKeyFile.load_from_bytes(
                    Gio.resources_lookup_data(
                        "/com/github/alex11br/themechanger/default.kvconfig",
                        Gio.ResourceLookupFlags.NONE
                    ),
                    GLib.KeyFileFlags.NONE
                )
            kvantumThemeKeyFile.set_boolean("Hacks", "iconless_pushbutton", not props.gtk_button_images)
            kvantumThemeKeyFile.set_boolean("Hacks", "iconless_menu", not props.gtk_menu_images)
            kvantumThemeKeyFile.set_boolean("%General", "transient_scrollbar", props.gtk_overlay_scrolling)

            kvantumThemeDir = os.path.join(GLib.get_user_config_dir(), "Kvantum", kvantumTheme+"#")
            os.makedirs(kvantumThemeDir, exist_ok=True)
            kvantumThemeKeyFile.save_to_file(os.path.join(kvantumThemeDir, kvantumTheme+"#.kvconfig"))

            kvantumKeyFile = GLib.KeyFile()
            kvantumKeyFile.set_string("General", "theme", kvantumTheme+"#")
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

class GSettingsApplyThemes(BaseApplyThemes):
    """
    Common live reloadable theme setting code for GSettings-based DE's i.e. Gnome, Cinnamon, Mate.

    self.settings gets defined by the derived classes tailored for each DE.
    """
    def applyThemes(self, props, **kwargs):
        super().applyThemes(props, **kwargs)

        self.settings.set_string("gtk-theme", props.gtk_theme_name)
        self.settings.set_string("icon-theme", props.gtk_icon_theme_name)
        self.settings.set_string("gtk-key-theme", props.gtk_key_theme_name or "")
        self.settings.set_string("font-name", props.gtk_font_name)
        
class MateApplyThemes(GSettingsApplyThemes):
    """
    Live reloadable theme & options setting code specific to Mate.
    """
    def __init__(self):
        self.settings = Gio.Settings.new("org.mate.interface")
        self.settingsCursor = Gio.Settings.new("org.mate.peripherals-mouse")
        self.settingsFont = Gio.Settings.new("org.mate.font-rendering")

    def applyThemes(self, props, **kwargs):
        super().applyThemes(props, **kwargs)

        self.settingsCursor.set_string("cursor-theme", props.gtk_cursor_theme_name or "")
        self.settingsCursor.set_int("cursor-size", props.gtk_cursor_theme_size)
        self.settingsFont.set_double("dpi", props.gtk_xft_dpi/1024)

        if props.gtk_xft_rgba != "none":
            self.settingsFont.set_string("rgba-order", props.gtk_xft_rgba)
            self.settingsFont.set_string("antialiasing", "rgba" if props.gtk_xft_antialias else "none")
        else:
            self.settingsFont.set_string("antialiasing", "grayscale" if props.gtk_xft_antialias else "none")
        self.settingsFont.set_string("hinting", props.gtk_xft_hintstyle[4:]) # drop the first 4 letters ('hint' in all cases)
        
        self.settings.set_boolean("gtk-overlay-scrolling", props.gtk_overlay_scrolling)
        self.settings.set_boolean("buttons-have-icons", props.gtk_button_images)
        self.settings.set_boolean("menus-have-icons", props.gtk_menu_images)

class CinnGnomeApplyThemes(GSettingsApplyThemes):
    """
    Common live reloadable theme setting code for Gnome & Cinnamon.
    """
    def applyThemes(self, props, **kwargs):
        super().applyThemes(props, **kwargs)

        self.settings.set_string("cursor-theme", props.gtk_cursor_theme_name or "")
        self.settings.set_int("cursor-size", props.gtk_cursor_theme_size)
        self.settings.set_double("text-scaling-factor", props.gtk_xft_dpi/(96*1024))

class GnomeApplyThemes(CinnGnomeApplyThemes):
    """
    Live reloadable theme & options setting code specific to Cinnamon.
    """
    def __init__(self):
        self.settings = Gio.Settings.new("org.gnome.desktop.interface")
    
    def applyThemes(self, props, **kwargs):
        super().applyThemes(props, **kwargs)

        if props.gtk_xft_rgba != "none":
            self.settings.set_string("font-rgba-order", props.gtk_xft_rgba or "rgb")
            self.settings.set_string("font-antialiasing", "rgba" if props.gtk_xft_antialias else "none")
        else:
            self.settings.set_string("font-antialiasing", "grayscale" if props.gtk_xft_antialias else "none")
        self.settings.set_string("font-hinting", props.gtk_xft_hintstyle[4:]) # drop the first 4 letters ('hint' in all cases)

        self.settings.set_boolean("overlay-scrolling", props.gtk_overlay_scrolling)

class CinnamonApplyThemes(CinnGnomeApplyThemes):
    """
    Live reloadable theme & options setting code specific to Gnome.
    """
    def __init__(self):
        self.settings = Gio.Settings.new("org.cinnamon.desktop.interface")
        self.settingsFont = Gio.Settings.new("org.cinnamon.settings-daemon.plugins.xsettings")

    def applyThemes(self, props, **kwargs):
        super().applyThemes(props, **kwargs)

        if props.gtk_xft_rgba != "none":
            self.settingsFont.set_string("rgba-order", props.gtk_xft_rgba)
            self.settingsFont.set_string("antialiasing", "rgba" if props.gtk_xft_antialias else "none")
        else:
            self.settingsFont.set_string("antialiasing", "grayscale" if props.gtk_xft_antialias else "none")
        self.settingsFont.set_string("hinting", props.gtk_xft_hintstyle[4:]) # drop the first 4 letters ('hint' in all cases)

        self.settings.set_boolean("gtk-overlay-scrollbars", props.gtk_overlay_scrolling)
        self.settings.set_boolean("buttons-have-icons", props.gtk_button_images)
        self.settings.set_boolean("menus-have-icons", props.gtk_menu_images)

class XApplyThemes(BaseApplyThemes):
    """
    Common live reloadable theme setting code for mechanisms which use the XSETTINGS property names.
    They all have an 'X' somewhere, too.

    self.settings gets defined by the derived classes tailored for each mechanism.
    """
    def applyThemes(self, props, **kwargs):
        super().applyThemes(props, **kwargs)
        self.options = {
            "Net/ThemeName": props.gtk_theme_name,
            "Net/IconThemeName": props.gtk_icon_theme_name,
            "Xft/Antialias": props.gtk_xft_antialias,
            "Xft/Hinting": props.gtk_xft_hinting,
            "Xft/HintStyle": props.gtk_xft_hintstyle or "hintnone",
            "Xft/RGBA": props.gtk_xft_rgba or "none",
            "Xft/DPI": props.gtk_xft_dpi,
            "Gtk/CursorThemeName": props.gtk_cursor_theme_name or "",
            "Gtk/FontName": props.gtk_font_name,
            "Gtk/KeyThemeName": props.gtk_key_theme_name or "",
            "Gtk/OverlayScrolling": props.gtk_overlay_scrolling,
            "Gtk/MenuImages": props.gtk_menu_images,
            "Gtk/ButtonImages": props.gtk_button_images,
        }

class LXSessionApplyThemes(XApplyThemes):
    """
    Live reloadable theme & options setting code specific to LXSession @ LXDE.
    """
    def __init__(self):
        self.lxsessionConfigPath = os.path.join(
            GLib.get_user_config_dir(),
            "lxsession",
            "LXDE",
            "desktop.conf"
        )

    def applyThemes(self, props, **kwargs):
        super().applyThemes(props, **kwargs)
        
        lxsessionKeyFile = GLib.KeyFile()
        lxsessionKeyFile.load_from_file(self.lxsessionConfigPath, GLib.KeyFileFlags.NONE)

        for option in self.options:
            value = self.options[option]
            
            if type(value) is str:
                lxsessionKeyFile.set_string("GTK", "s"+option, value)
            else:
                lxsessionKeyFile.set_integer("GTK", "i"+option, int(value))
        
        lxsessionKeyFile.save_to_file(self.lxsessionConfigPath)

class XfconfApplyThemes(XApplyThemes):
    """
    Live reloadable theme & options setting code specific to Xfconf @ XFCE.
    """
    def setOption(self, option, value):
        subprocess.run([
            "xfconf-query", "-c", "xsettings",
            "-p", option,
            "-s", value
        ])

    def applyThemes(self, props, **kwargs):
        super().applyThemes(props, **kwargs)

        for option in self.options:
            value = self.options[option]
            
            if option == "Xft/DPI":
                value = int(value/1024)
            if type(value) is int:
                value = str(value)
            elif value == True:
                value = "true"
            elif value == False:
                value = "false"

            self.setOption("/"+option, value)

class XsettingsdApplyThemes(XApplyThemes):
    """
    Live reloadable theme & options setting code specific to xsettingsd.
    """
    def __init__(self):
        self.confFolder = os.path.join(GLib.get_user_config_dir(), "xsettingsd")
        try:
            os.mkdir(self.confFolder)
        except:
            pass
        self.confFile = os.path.join(self.confFolder, "xsettingsd.conf")

    def applyThemes(self, props, **kwargs):
        super().applyThemes(props, **kwargs)

        with open(self.confFile, "w") as file:
            for option in self.options:
                value = self.options[option]
                
                if type(value) is str:
                    value = f'"{value}"'
                elif type(value) is bool:
                    value = int(value)
                
                file.write(f'{option} {value}\n')
        
        subprocess.run(["pkill", "-HUP", "^xsettingsd$"])

def isRunning(app):
    return subprocess.call(["pidof", app], stdout=subprocess.DEVNULL) == 0

def getThemeApplier():
    if isRunning("gsd-xsettings"):
        return GnomeApplyThemes()
    elif isRunning("csd-xsettings"):
        return CinnamonApplyThemes()
    elif isRunning("mate-settings-daemon"):
        return MateApplyThemes()
    elif isRunning("xfsettingsd"):
        return XfconfApplyThemes()
    elif isRunning("lxsession"):
        return LXSessionApplyThemes()
    elif isRunning("xsettingsd"):
        return XsettingsdApplyThemes()
    else:
        return BaseApplyThemes()
