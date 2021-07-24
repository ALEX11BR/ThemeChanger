import os
import configparser
import traceback
from gi.repository import Gtk, GLib

def uniquifySortedListStore(listStore):
    prev = None
    for row in listStore:
        if prev and prev[1] == row[1]:
            listStore.remove(prev.iter)
        prev = row
    return listStore

def getAvailableGtk3Themes():
    availableThemes = Gtk.ListStore(str, str)
    availableThemes.set_sort_column_id(0, Gtk.SortType.ASCENDING)
    availableThemes.append(["Adwaita", "Adwaita"])
    lookupPaths = [
        os.path.join(GLib.get_user_data_dir(), "themes"),
        os.path.join(GLib.get_home_dir(), ".themes"),
        "/usr/share/themes"
    ]
    for lookupPath in lookupPaths:
        try:
            for f in os.listdir(lookupPath):
                if os.path.isfile(os.path.join(lookupPath, f, "gtk-3.0", "gtk.css")):
                    availableThemes.append([f, f])
        except:
            pass
    return uniquifySortedListStore(availableThemes)

def getAvailableIconThemes():
    availableThemes = Gtk.ListStore(str, str)
    availableThemes.set_sort_column_id(0, Gtk.SortType.ASCENDING)
    lookupPaths = [
        os.path.join(GLib.get_user_data_dir(), "icons"),
        os.path.join(GLib.get_home_dir(), ".icons"),
        "/usr/share/icons"
    ]
    for lookupPath in lookupPaths:
        try:
            for f in os.listdir(lookupPath):
                if f != "default":
                    try:
                        themeFileParser = GLib.KeyFile()
                        themeFileParser.load_from_file(os.path.join(lookupPath, f, "index.theme"), GLib.KeyFileFlags.NONE)
                        if (themeFileParser.get_string("Icon Theme", "Directories")):
                            availableThemes.append([themeFileParser.get_locale_string("Icon Theme", "Name"), f])
                    except:
                        pass
        except:
            pass
    return uniquifySortedListStore(availableThemes)

def getAvailableCursorThemes():
    availableThemes = Gtk.ListStore(str, str)
    availableThemes.set_sort_column_id(0, Gtk.SortType.ASCENDING)
    lookupPaths = [
        os.path.join(GLib.get_user_data_dir(), "icons"),
        os.path.join(GLib.get_home_dir(), ".icons"),
        "/usr/share/icons"
    ]
    for lookupPath in lookupPaths:
        try:
            for f in os.listdir(lookupPath):
                if f != "default" and os.path.isdir(os.path.join(lookupPath, f, "cursors")):
                    try:
                        themeFileParser = GLib.KeyFile()
                        themeFileParser.load_from_file(os.path.join(lookupPath, f, "index.theme"), GLib.KeyFileFlags.NONE)
                        availableThemes.append([themeFileParser.get_locale_string("Icon Theme", "Name"), f])
                    except:
                        pass
        except:
            pass
    return uniquifySortedListStore(availableThemes)

def getAvailableGtk4Themes():
    availableThemes = Gtk.ListStore(str, str)
    availableThemes.set_sort_column_id(0, Gtk.SortType.ASCENDING)
    availableThemes.append(["Adwaita", "Adwaita"])
    lookupPaths = [
        os.path.join(GLib.get_user_data_dir(), "themes"),
        os.path.join(GLib.get_home_dir(), ".themes"),
        "/usr/share/themes"
    ]
    for lookupPath in lookupPaths:
        try:
            for f in os.listdir(lookupPath):
                if os.path.isfile(os.path.join(lookupPath, f, "gtk-4.0", "gtk.css")):
                    availableThemes.append([f, f])
        except:
            pass
    return uniquifySortedListStore(availableThemes)

def getAvailableGtk2Themes():
    availableThemes = Gtk.ListStore(str, str)
    availableThemes.set_sort_column_id(0, Gtk.SortType.ASCENDING)
    lookupPaths = [
        os.path.join(GLib.get_user_data_dir(), "themes"),
        os.path.join(GLib.get_home_dir(), ".themes"),
        "/usr/share/themes"
    ]
    for lookupPath in lookupPaths:
        try:
            for f in os.listdir(lookupPath):
                if os.path.isfile(os.path.join(lookupPath, f, "gtk-2.0", "gtkrc")):
                    availableThemes.append([f, f])
        except:
            pass
    return uniquifySortedListStore(availableThemes)