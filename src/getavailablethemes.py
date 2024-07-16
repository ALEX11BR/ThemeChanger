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
from pathlib import Path
from gi.repository import Gtk, GLib, GdkPixbuf

from .pixbuffromxcursor import pixbufFromXCursor

def uniquifySortedListStore(listStore):
    prev = None
    for row in listStore:
        if prev and prev[1] == row[1]:
            listStore.remove(prev.iter)
        prev = row
    return listStore

"""
The functions below create Gtk.ListStore's that store themes
for use in SearchableThemeList's and have the following columns:
0. A str column which holds the display name of the theme
1. A str column which holds the underlying theme name
2. A str column which holds the theme file/folder path (those starting in "//" are fake ones that show a lack of a theme file)
3. (Optional) A GdkPixbuf.Pixbuf column which holds the theme's preview image
"""

def getAvailableGtk3Themes():
    availableThemes = Gtk.ListStore(str, str, str, GdkPixbuf.Pixbuf)
    availableThemes.set_sort_column_id(0, Gtk.SortType.ASCENDING)
    availableThemes.append([" Adwaita", "Adwaita", "//none",
        GdkPixbuf.Pixbuf.new_from_resource(
            "/com/github/alex11br/themechanger/adwaita.png"
        )
    ])
    lookupPaths = [
        os.path.join(GLib.get_user_data_dir(), "themes"),
        os.path.join(GLib.get_home_dir(), ".themes"),
    ] + [os.path.join(dataDir, "themes") for dataDir in GLib.get_system_data_dirs()]
    for lookupPath in lookupPaths:
        try:
            for f in os.listdir(lookupPath):
                if f != "Adwaita" and os.path.isfile(os.path.join(lookupPath, f, "gtk-3.0", "gtk.css")):
                    thumbnailFile = os.path.join(lookupPath, f, "gtk-3.0", "thumbnail.png")
                    availableThemes.append([
                        # we add a space to the beginning of the display name
                        # to create spacing between the theme preview image and the theme name text
                        " "+f, f, os.path.join(lookupPath, f),
                        GdkPixbuf.Pixbuf.new_from_file_at_size(
                            thumbnailFile, 120, 35
                        ) if os.path.isfile(thumbnailFile) else GdkPixbuf.Pixbuf.new_from_resource(
                            "/com/github/alex11br/themechanger/unknown.png"
                        )
                    ])
        except:
            pass
    return uniquifySortedListStore(availableThemes)

def getAvailableIconThemes():
    availableThemes = Gtk.ListStore(str, str, str, GdkPixbuf.Pixbuf)
    availableThemes.set_sort_column_id(0, Gtk.SortType.ASCENDING)
    lookupPaths = [
        os.path.join(GLib.get_user_data_dir(), "icons"),
        os.path.join(GLib.get_home_dir(), ".icons"),
    ] + [os.path.join(dataDir, "icons") for dataDir in GLib.get_system_data_dirs()]
    for lookupPath in lookupPaths:
        try:
            for f in os.listdir(lookupPath):
                if f != "default":
                    iconTheme = Gtk.IconTheme.new()
                    iconTheme.set_custom_theme(f)
                    try:
                        themeFileParser = GLib.KeyFile()
                        themeFileParser.load_from_file(
                            os.path.join(lookupPath, f, "index.theme"), GLib.KeyFileFlags.NONE
                        )
                        if (themeFileParser.get_string("Icon Theme", "Directories")):
                            availableThemes.append([
                                themeFileParser.get_locale_string("Icon Theme", "Name"), f, os.path.join(lookupPath, f),
                                iconTheme.load_icon(
                                    iconTheme.get_example_icon_name(),
                                    32, Gtk.IconLookupFlags.FORCE_SIZE
                                )
                            ])
                    except:
                        pass
        except:
            pass
    return uniquifySortedListStore(availableThemes)

def getAvailableCursorThemes():
    availableThemes = Gtk.ListStore(str, str, str, GdkPixbuf.Pixbuf)
    availableThemes.set_sort_column_id(0, Gtk.SortType.ASCENDING)
    availableThemes.append([
        "Default cursor", "default", "//none",
        GdkPixbuf.Pixbuf.new_from_resource(
            "/com/github/alex11br/themechanger/defaultcursor.png"
        )
    ])
    lookupPaths = [
        os.path.join(GLib.get_user_data_dir(), "icons"),
        os.path.join(GLib.get_home_dir(), ".icons"),
    ] + [os.path.join(dataDir, "icons") for dataDir in GLib.get_system_data_dirs()]
    for lookupPath in lookupPaths:
        try:
            for f in os.listdir(lookupPath):
                if f != "default" and os.path.isdir(os.path.join(lookupPath, f, "cursors")):
                    cursorPath = os.path.join(lookupPath, f, "cursors", "left_ptr")
                    try:
                        themeFileParser = GLib.KeyFile()
                        themeFileParser.load_from_file(
                            os.path.join(lookupPath, f, "index.theme"), GLib.KeyFileFlags.NONE
                        )
                        availableThemes.append([
                            themeFileParser.get_locale_string("Icon Theme", "Name"), f, os.path.join(lookupPath, f),
                            pixbufFromXCursor(
                                cursorPath
                            ) if os.path.isfile(cursorPath) else GdkPixbuf.Pixbuf.new_from_resource(
                                "/com/github/alex11br/themechanger/defaultcursor.png"
                            )
                        ])
                    except:
                        pass
        except:
            pass
    return uniquifySortedListStore(availableThemes)

def getAvailableGtk4Themes():
    availableThemes = Gtk.ListStore(str, str, str)
    availableThemes.set_sort_column_id(0, Gtk.SortType.ASCENDING)
    availableThemes.append(["Adwaita", "Adwaita", "//none"])
    lookupPaths = [
        os.path.join(GLib.get_user_data_dir(), "themes"),
        os.path.join(GLib.get_home_dir(), ".themes"),
    ] + [os.path.join(dataDir, "themes") for dataDir in GLib.get_system_data_dirs()]
    for lookupPath in lookupPaths:
        try:
            for f in os.listdir(lookupPath):
                if os.path.isfile(os.path.join(lookupPath, f, "gtk-4.0", "gtk.css")):
                    availableThemes.append([f, f, os.path.join(lookupPath, f)])
        except:
            pass
    return uniquifySortedListStore(availableThemes)

def getAvailableGtk2Themes():
    availableThemes = Gtk.ListStore(str, str, str)
    availableThemes.set_sort_column_id(0, Gtk.SortType.ASCENDING)
    lookupPaths = [
        os.path.join(GLib.get_user_data_dir(), "themes"),
        os.path.join(GLib.get_home_dir(), ".themes"),
    ] + [os.path.join(dataDir, "themes") for dataDir in GLib.get_system_data_dirs()]
    for lookupPath in lookupPaths:
        try:
            for f in os.listdir(lookupPath):
                if os.path.isfile(os.path.join(lookupPath, f, "gtk-2.0", "gtkrc")):
                    availableThemes.append([f, f, os.path.join(lookupPath, f)])
        except:
            pass
    return uniquifySortedListStore(availableThemes)

def getAvailableKvantumThemes(kvantumPath):
    availableThemes = Gtk.ListStore(str, str, str)
    availableThemes.set_sort_column_id(0, Gtk.SortType.ASCENDING)
    # The default kvantum theme file is not available as a regular file in the filesystem
    # but rather bundled in a QT resource with Kvantum.
    # We'll consider its file to be '//default', which cannot exist due to the double slash
    # and handle this case particularly when applying the kvantum theme.
    availableThemes.append(["Kvantum", "Default", "//default"])
    lookupPaths = [
        os.path.join(GLib.get_user_config_dir(), "Kvantum"),
        os.path.join(Path(kvantumPath).parent.parent, "share", "Kvantum")
    ]
    for lookupPath in lookupPaths:
        try:
            for f in os.listdir(lookupPath):
                themeFilePath = os.path.join(lookupPath, f, f+".kvconfig")
                if "#" not in f and os.path.isfile(themeFilePath):
                    availableThemes.append([f, f, themeFilePath])
                    darkThemePath = os.path.join(lookupPath, f, f+"Dark.kvconfig")
                    if os.path.isfile(darkThemePath):
                        availableThemes.append([f+"Dark", f+"Dark", darkThemePath])
        except:
            pass
    return uniquifySortedListStore(availableThemes)
