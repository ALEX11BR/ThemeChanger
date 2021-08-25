import os
import configparser
import traceback
from gi.repository import Gtk, GLib, GdkPixbuf

def uniquifySortedListStore(listStore):
    prev = None
    for row in listStore:
        if prev and prev[1] == row[1]:
            listStore.remove(prev.iter)
        prev = row
    return listStore

def getAvailableGtk3Themes():
    availableThemes = Gtk.ListStore(str, str, GdkPixbuf.Pixbuf)
    availableThemes.set_sort_column_id(0, Gtk.SortType.ASCENDING)
    availableThemes.append([" Adwaita", "Adwaita",
        GdkPixbuf.Pixbuf.new_from_resource(
            "/com/github/alex11br/themechanger/adwaita.png"
        )
    ])
    lookupPaths = [
        os.path.join(GLib.get_user_data_dir(), "themes"),
        os.path.join(GLib.get_home_dir(), ".themes"),
        "/usr/share/themes"
    ]
    for lookupPath in lookupPaths:
        try:
            for f in os.listdir(lookupPath):
                if f != "Adwaita" and os.path.isfile(os.path.join(lookupPath, f, "gtk-3.0", "gtk.css")):
                    thumbnailFile = os.path.join(lookupPath, f, "gtk-3.0", "thumbnail.png")
                    availableThemes.append([
                        " "+f, f,
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
    availableThemes = Gtk.ListStore(str, str, GdkPixbuf.Pixbuf)
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
                    iconTheme = Gtk.IconTheme.new()
                    iconTheme.set_custom_theme(f)
                    try:
                        themeFileParser = GLib.KeyFile()
                        themeFileParser.load_from_file(
                            os.path.join(lookupPath, f, "index.theme"), GLib.KeyFileFlags.NONE
                        )
                        if (themeFileParser.get_string("Icon Theme", "Directories")):
                            availableThemes.append([
                                themeFileParser.get_locale_string("Icon Theme", "Name"), f,
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
    availableThemes = Gtk.ListStore(str, str)
    availableThemes.set_sort_column_id(0, Gtk.SortType.ASCENDING)
    availableThemes.append(["Default cursor", "default"])
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