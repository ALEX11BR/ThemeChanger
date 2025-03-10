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
import shutil

from gi.repository import Gtk, Gdk, GLib

from .applythemes import getThemeApplier, BaseApplyThemes
from .installthemes import showArchiveChooserDialog, showErrorDialog, showSuccessDialog, installThemeArchive, checkIconIndexFile, checkKvantumFile
from .getavailablethemes import getAvailableGtk3Themes, getAvailableIconThemes, getAvailableCursorThemes, getAvailableGtk2Themes, getAvailableGtk4Themes, getAvailableKvantumThemes
from .searchablethemelist import SearchableThemeList

@Gtk.Template(resource_path='/com/github/alex11br/themechanger/window.ui')
class ThemechangerWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ThemechangerWindow'

    gtkProps = Gtk.Settings.get_default().props

    defaultDisplay = Gdk.Display.get_default()
    defaultScreen = Gdk.Screen.get_default()

    widgetsSectionScrolledWindow = Gtk.Template.Child()
    gtkThemesBox = Gtk.Template.Child()
    iconThemesBox = Gtk.Template.Child()
    cursorThemesBox = Gtk.Template.Child()
    darkVariantSwitch = Gtk.Template.Child()
    emacsShortcutsSwitch = Gtk.Template.Child()
    overlayScrollbarsSwitch = Gtk.Template.Child()
    xsettingsInfoBar = Gtk.Template.Child()
    anotherGtk2ThemeBox = Gtk.Template.Child()
    anotherGtk2ThemeSwitch = Gtk.Template.Child()
    anotherGtk4ThemeBox = Gtk.Template.Child()
    anotherGtk4ThemeSwitch = Gtk.Template.Child()
    kvantumThemeBox = Gtk.Template.Child()
    anotherKvantumThemeSwitch = Gtk.Template.Child()
    menuImagesSwitch = Gtk.Template.Child()
    buttonImagesSwitch = Gtk.Template.Child()
    customCursorSizeSwitch = Gtk.Template.Child()
    customCursorSizeScale = Gtk.Template.Child()
    customCursorSizeBox = Gtk.Template.Child()
    antialiasingSwitch = Gtk.Template.Child()
    fontButton = Gtk.Template.Child()
    dpiButton = Gtk.Template.Child()
    hintingCombobox = Gtk.Template.Child()
    subpixelCombobox = Gtk.Template.Child()
    cssTextBuffer = Gtk.Template.Child()
    kvantumThemeInstallButton = Gtk.Template.Child()

    gtkThemesApplyButton = Gtk.Template.Child()
    iconThemesApplyButton = Gtk.Template.Child()
    cursorThemesApplyButton = Gtk.Template.Child()
    editCssApplyButton = Gtk.Template.Child()
    otherOptionsApplyButton = Gtk.Template.Child()

    def __init__(self, app):
        super().__init__(title="Theme Changer", application=app)

        # To properly have CSS live reloading, we'll have to handle the case in which properties form an existing CSS file get deleted, e.g.
        ######################    ######################
        # background: green; # -> # /* gone */         #
        ######################    ######################
        # GTK still loads these properties during the app initialization at the highest priority,
        # and even if the user deletes them, they still remain set there in the loaded CSS properties and thus still have effect.
        # To address this, at the highest priority we'll have to add first an all-round unsetter...
        self.unsetterCssProvider = Gtk.CssProvider()
        self.unsetterCssProvider.load_from_data(b"""
            * {
                all: unset;
            }
        """)
        Gtk.StyleContext.add_provider_for_screen(
            self.defaultScreen, self.unsetterCssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )
        # Now we'll start putting the CSS providers that normally exist in a GTK application: the one with the GTK theme...
        self.gtkThemeCssProvider = Gtk.CssProvider.get_named(self.gtkProps.gtk_theme_name, "dark" if self.gtkProps.gtk_application_prefer_dark_theme else None)
        Gtk.StyleContext.add_provider_for_screen(
            self.defaultScreen, self.gtkThemeCssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )
        # ...and the GTK settings, a provider in and of itself
        # TODO: The add_provider method from a dedicated instance doesn't work at all for any style provider, and this one crashes the app
        # Without the gtk settings, we'll have to do some extra work to instantly reload gtk themes i.e to updateGtkThemeCssProvider
        """
        Gtk.StyleContext.add_provider_for_screen(
            self.defaultScreen, Gtk.Settings.get_default(), Gtk.STYLE_PROVIDER_PRIORITY_USER
        )
        """
        # Now we'll add the CSS provider that will change as the user types in the textbox
        # Its value will get set automatically as we set the cssTextBuffer text, as a part of the set_text signal
        # We'll ensure first that the current working directory is the one with the CSS's in them to make sure @import's work as intended
        os.chdir(os.path.join(GLib.get_user_config_dir(), "gtk-3.0"))
        self.cssProvider = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_screen(
            self.defaultScreen, self.cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER+1
            # A higher priority than the USER one, to allow a theme change without requiring heavy meddling with the cssProvider
        )

        # Now we'll set up the widgets
        try:
            with open(os.path.join(GLib.get_user_config_dir(), "gtk-3.0", "gtk.css"), "r") as cssFile:
                self.cssTextBuffer.set_text(cssFile.read())
        # If the CSS file doesn't exist (or we are unable to access it for reading), we'll set up a nice text placeholder
        except:
            self.cssTextBuffer.set_text("")

        self.themeApplier = getThemeApplier()
        if type(self.themeApplier) == BaseApplyThemes:
            self.xsettingsInfoBar.set_visible(False)

        self.gtkSearchableThemeList = SearchableThemeList(
            getAvailableGtk3Themes(),
            self.gtkProps.gtk_theme_name,
            self.onGtkThemeChanged,
            hasPixbuf=True
        )
        self.gtkThemesBox.pack_start(self.gtkSearchableThemeList, True, True, 0)

        self.iconSearchableThemeList = SearchableThemeList(
            getAvailableIconThemes(),
            self.gtkProps.gtk_icon_theme_name,
            self.onIconThemeChanged,
            hasPixbuf=True
        )
        self.iconThemesBox.pack_start(self.iconSearchableThemeList, True, True, 0)

        self.cursorSearchableThemeList = SearchableThemeList(
            getAvailableCursorThemes(),
            self.gtkProps.gtk_cursor_theme_name or "default",
            self.onCursorThemeChanged,
            hasPixbuf=True
        )
        self.cursorThemesBox.pack_start(self.cursorSearchableThemeList, True, True, 0)

        try:
            with open(os.path.join(GLib.get_home_dir(), ".gtkrc-2.0"), "r") as gtk2File:
                gtk2KeyFile = GLib.KeyFile()
                gtk2KeyFile.load_from_bytes(GLib.Bytes(b"[Settings]\n"+gtk2File.read().encode()), GLib.KeyFileFlags.NONE)
                self.gtk2ThemeName = gtk2KeyFile.get_string("Settings", "gtk-theme-name").strip('"')
        except:
            self.gtk2ThemeName = self.gtkProps.gtk_theme_name
        hasAnotherGtk2Theme = self.gtkProps.gtk_theme_name != self.gtk2ThemeName
        self.gtk2SearchableThemeList = SearchableThemeList(
            getAvailableGtk2Themes(),
            self.gtk2ThemeName,
            self.onGtk2ThemeChanged
        )
        self.anotherGtk2ThemeBox.pack_start(self.gtk2SearchableThemeList, True, True, 0)
        self.anotherGtk2ThemeSwitch.set_active(hasAnotherGtk2Theme)
        self.gtk2SearchableThemeList.set_visible(hasAnotherGtk2Theme)

        try:
            gtk4KeyFile = GLib.KeyFile()
            gtk4KeyFile.load_from_file(os.path.join(GLib.get_user_config_dir(), "gtk-4.0", "settings.ini"), GLib.KeyFileFlags.NONE)
            self.gtk4ThemeName = gtk4KeyFile.get_string("Settings", "gtk-theme-name")
        except:
            self.gtk4ThemeName = self.gtkProps.gtk_theme_name
        hasAnotherGtk4Theme = self.gtkProps.gtk_theme_name != self.gtk4ThemeName
        self.gtk4SearchableThemeList = SearchableThemeList(
            getAvailableGtk4Themes(),
            self.gtk4ThemeName,
            self.onGtk4ThemeChanged
        )
        self.anotherGtk4ThemeBox.pack_start(self.gtk4SearchableThemeList, True, True, 0)
        self.anotherGtk4ThemeSwitch.set_active(hasAnotherGtk4Theme)
        self.gtk4SearchableThemeList.set_visible(hasAnotherGtk4Theme)

        kvantumPath = shutil.which("kvantummanager")
        if kvantumPath:
            try:
                kvantumKeyFile = GLib.KeyFile()
                kvantumKeyFile.load_from_file(os.path.join(GLib.get_user_config_dir(), "Kvantum", "kvantum.kvconfig"), GLib.KeyFileFlags.NONE)
                self.kvantumThemeName = kvantumKeyFile.get_string("General", "theme")
                if self.kvantumThemeName[-1] == "#":
                    # drop the last character i.e. '#', the 'changed theme' modifier
                    self.kvantumThemeName = self.kvantumThemeName[:-1]
            except:
                self.kvantumThemeName = "Default"
            hasAnotherKvantumTheme = self.gtkProps.gtk_theme_name != self.kvantumThemeName
            self.kvantumThemeFilePath = "//notset"
            # When we run the constructor for the kvantumSearchableThemeList,
            # its TreeSelection's selected item will be set to the one matching the kvantumThemeName
            # thus triggering the 'changed' signal's function, which then calls the callback
            # with the 2 params of the selected item, thus properly setting the kvantumThemeName.
            self.kvantumSearchableThemeList = SearchableThemeList(
                getAvailableKvantumThemes(kvantumPath),
                self.kvantumThemeName,
                self.onKvantumThemeChanged,
                hasThemeFilePath=True
            )
            self.kvantumThemeBox.pack_start(self.kvantumSearchableThemeList, True, True, 0)
            self.anotherKvantumThemeSwitch.set_active(hasAnotherKvantumTheme)
            self.kvantumSearchableThemeList.set_visible(hasAnotherKvantumTheme)
        else:
            self.kvantumThemeBox.set_visible(False)
            self.kvantumThemeInstallButton.set_visible(False)
            self.kvantumThemeFilePath = "//notthecase"

        self.darkVariantSwitch.set_active(self.gtkProps.gtk_application_prefer_dark_theme)

        self.emacsShortcutsSwitch.set_active(self.gtkProps.gtk_key_theme_name == 'Emacs')

        self.overlayScrollbarsSwitch.set_active(not self.gtkProps.gtk_overlay_scrolling)

        self.menuImagesSwitch.set_active(self.gtkProps.gtk_menu_images)

        self.buttonImagesSwitch.set_active(self.gtkProps.gtk_button_images)

        self.customCursorSizeSwitch.set_active(bool(self.gtkProps.gtk_cursor_theme_size))
        self.customCursorSizeBox.set_visible(bool(self.gtkProps.gtk_cursor_theme_size))
        self.customCursorSizeScale.set_value(self.gtkProps.gtk_cursor_theme_size)

        self.antialiasingSwitch.set_active(bool(self.gtkProps.gtk_xft_antialias))

        self.fontButton.set_font(self.gtkProps.gtk_font_name)

        self.dpiButton.set_value(self.gtkProps.gtk_xft_dpi / 1024)

        self.hintingCombobox.set_active_id(self.gtkProps.gtk_xft_hintstyle if (self.gtkProps.gtk_xft_hinting != 0) else "hintnone")

        self.subpixelCombobox.set_active_id(self.gtkProps.gtk_xft_rgba or "none")


    def updateGtkThemeCssProvider(self):
        gtkThemeCssProvider = Gtk.CssProvider.get_named(self.gtkProps.gtk_theme_name, "dark" if self.gtkProps.gtk_application_prefer_dark_theme else None)
        Gtk.StyleContext.remove_provider_for_screen(self.defaultScreen, self.gtkThemeCssProvider)
        Gtk.StyleContext.add_provider_for_screen(
            self.defaultScreen, gtkThemeCssProvider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )
        self.gtkThemeCssProvider = gtkThemeCssProvider

    def setDefaultCursor(self):
        # This makes the cursor update to the recently selected theme
        defaultCursor = Gdk.Cursor.new_for_display(self.defaultDisplay, Gdk.CursorType.LEFT_PTR)
        self.defaultScreen.get_root_window().set_cursor(defaultCursor)

    def getGtk4ThemeCssPath(self):
        if self.anotherGtk4ThemeSwitch.get_active():
            gtk4ThemeRoot = self.gtk4SearchableThemeList.selectedThemeRow[2]
        else:
            gtk4ThemeRoot = self.gtkSearchableThemeList.selectedThemeRow[2]

        if gtk4ThemeRoot[:2] == "//":
            return None

        gtk4ThemeCssPath = os.path.join(gtk4ThemeRoot, "gtk-4.0", "gtk-dark.css" if self.gtkProps.gtk_application_prefer_dark_theme else "gtk.css")
        if not os.path.isfile(gtk4ThemeCssPath):
            gtk4ThemeCssPath = os.path.join(gtk4ThemeRoot, "gtk-4.0", "gtk.css")
            if not os.path.isfile(gtk4ThemeCssPath):
                return None
        return gtk4ThemeCssPath

    def onGtkThemeChanged(self, themename):
        self.onSettingChanged()

        self.gtkProps.gtk_theme_name = themename
        if not self.anotherGtk2ThemeSwitch.get_active():
            self.gtk2ThemeName = themename
        if not self.anotherGtk4ThemeSwitch.get_active():
            self.gtk4ThemeName = themename
        if self.kvantumThemeBox.get_visible() and not self.anotherKvantumThemeSwitch.get_active():
            self.kvantumThemeName = themename

        self.updateGtkThemeCssProvider()

    def onIconThemeChanged(self, themename):
        self.onSettingChanged()
        self.gtkProps.gtk_icon_theme_name = themename

    def onCursorThemeChanged(self, themename):
        self.onSettingChanged()
        self.gtkProps.gtk_cursor_theme_name = None if themename == "default" else themename
        self.setDefaultCursor()

    def onGtk2ThemeChanged(self, themename):
        self.onSettingChanged()
        self.gtk2ThemeName = themename

    def onGtk4ThemeChanged(self, themename):
        self.onSettingChanged()
        self.gtk4ThemeName = themename

    def onKvantumThemeChanged(self, themename, themepath):
        self.onSettingChanged()
        self.kvantumThemeName = themename
        self.kvantumThemeFilePath = themepath

    @Gtk.Template.Callback()
    def darkVariantSwitchStateSet(self, switch, state):
        self.gtkProps.gtk_application_prefer_dark_theme = state
        self.updateGtkThemeCssProvider()

    @Gtk.Template.Callback()
    def emacsShortcutsSwitchStateSet(self, switch, state):
        self.gtkProps.gtk_key_theme_name = 'Emacs' if state else ''

    @Gtk.Template.Callback()
    def overlayScrollbarsSwitchStateSet(self, switch, state):
        self.gtkProps.gtk_overlay_scrolling = not state
        # To see this setting in effect, one must move to an other page besides the 'widgets' tab (then they can come back)
        # We can remove this necessity by updating the overlay scrolling setting for those in the 'widgets' tab that have it
        self.widgetsSectionScrolledWindow.set_overlay_scrolling(not state)
        self.gtkSearchableThemeList.setScrolledWindowOverlayScrolling(not state)
        self.gtk2SearchableThemeList.setScrolledWindowOverlayScrolling(not state)
        self.gtk4SearchableThemeList.setScrolledWindowOverlayScrolling(not state)
        if self.kvantumThemeBox.get_visible():
            self.kvantumSearchableThemeList.setScrolledWindowOverlayScrolling(not state)

    @Gtk.Template.Callback()
    def anotherGtk2ThemeSwitchStateSet(self, switch, state):
        self.gtk2ThemeName = self.gtk2SearchableThemeList.selectedTheme if state else self.gtkProps.gtk_theme_name
        self.gtk2SearchableThemeList.set_visible(state)

    @Gtk.Template.Callback()
    def anotherGtk4ThemeSwitchStateSet(self, switch, state):
        self.gtk4ThemeName = self.gtk4SearchableThemeList.selectedTheme if state else self.gtkProps.gtk_theme_name
        self.gtk4SearchableThemeList.set_visible(state)

    @Gtk.Template.Callback()
    def anotherKvantumThemeSwitchStateSet(self, switch, state):
        self.kvantumThemeName = self.kvantumSearchableThemeList.selectedTheme if state else self.gtkProps.gtk_theme_name
        self.kvantumSearchableThemeList.set_visible(state)

    @Gtk.Template.Callback()
    def menuImagesSwitchStateSet(self, switch, state):
        self.gtkProps.gtk_menu_images = state

    @Gtk.Template.Callback()
    def buttonImagesSwitchStateSet(self, switch, state):
        self.gtkProps.gtk_button_images = state

    @Gtk.Template.Callback()
    def customCursorSizeSwitchStateSet(self, switch, state):
        self.gtkProps.gtk_cursor_theme_size = self.gtkProps.gtk_cursor_theme_size if state else 0
        self.customCursorSizeBox.set_visible(state)
        self.customCursorSizeScale.set_value(self.gtkProps.gtk_cursor_theme_size if state else 0)

    @Gtk.Template.Callback()
    def customCursorSizeScaleValueChanged(self, scale):
        self.gtkProps.gtk_cursor_theme_size = scale.get_value()
        self.setDefaultCursor()

    @Gtk.Template.Callback()
    def antialiasingSwitchStateSet(self, switch, state):
        self.gtkProps.gtk_xft_antialias = int(state)

    @Gtk.Template.Callback()
    def fontButtonFontSet(self, button):
        self.gtkProps.gtk_font_name = button.get_font()

    @Gtk.Template.Callback()
    def dpiButtonValueChanged(self, button):
        self.gtkProps.gtk_xft_dpi = button.get_value() * 1024

    @Gtk.Template.Callback()
    def hintingComboboxChanged(self, combobox):
        self.gtkProps.gtk_xft_hintstyle = combobox.get_active_id()
        self.gtkProps.gtk_xft_hinting = 1

    @Gtk.Template.Callback()
    def subpixelComboboxChanged(self, combobox):
        self.gtkProps.gtk_xft_rgba = combobox.get_active_id()

    @Gtk.Template.Callback()
    def onCssTextBufferChanged(self, buffer):
        self.cssProvider.load_from_data(buffer.props.text.encode())

    @Gtk.Template.Callback()
    def onDestroy(self, *args):
        self.close()

    @Gtk.Template.Callback()
    def applySettings(self, *args):
        self.gtkThemesApplyButton.set_sensitive(False)
        self.iconThemesApplyButton.set_sensitive(False)
        self.cursorThemesApplyButton.set_sensitive(False)
        self.editCssApplyButton.set_sensitive(False)
        self.otherOptionsApplyButton.set_sensitive(False)

        try:
            self.themeApplier.applyThemes(
                props=self.gtkProps,
                gtk2Theme=self.gtk2ThemeName,
                gtk4Theme=self.gtk4ThemeName,
                kvantumTheme=self.kvantumThemeName,
                kvantumThemeFilePath=self.kvantumThemeFilePath,
                cssText=self.cssTextBuffer.props.text,
                gtk4ThemePath=self.getGtk4ThemeCssPath()
            )
        except Exception as err:
            showErrorDialog("Error: Could not apply settings", str(err))
            self.onSettingChanged()

    def installArchive(self, kind, section, destination, anchorFile, anchorLevels, lookupFunction):
        archivePath = showArchiveChooserDialog(f'Select the {kind} theme archive file')
        if archivePath:
            try:
                installThemeArchive(kind, archivePath, destination, anchorFile, anchorLevels, lookupFunction)
            except Exception as err:
                showErrorDialog(
                    f"There have been issues while extracting the theme from the archive at '{archivePath}'.",
                    str(err)
                )
            else:
                showSuccessDialog(archivePath, section)

    @Gtk.Template.Callback()
    def installWidgetTheme(self, *args):
        self.installArchive(
            "widget", "Widgets",
            os.path.join(GLib.get_user_data_dir(), "themes"),
            "gtk-3.0/gtk.css", 2, lambda x: True
        )
        self.gtkSearchableThemeList.setThemesTreeViewModel(getAvailableGtk3Themes())
        self.gtk2SearchableThemeList.setThemesTreeViewModel(getAvailableGtk2Themes())
        self.gtk4SearchableThemeList.setThemesTreeViewModel(getAvailableGtk4Themes())

    @Gtk.Template.Callback()
    def installIconTheme(self, *args):
        self.installArchive(
            "icon", "Icons",
            os.path.join(GLib.get_user_data_dir(), "icons"),
            "index.theme", 1, checkIconIndexFile
        )
        self.iconSearchableThemeList.setThemesTreeViewModel(getAvailableIconThemes())
        self.cursorSearchableThemeList.setThemesTreeViewModel(getAvailableCursorThemes())

    @Gtk.Template.Callback()
    def installKvantumTheme(self, *args):
        self.installArchive(
            "Kvantum", "Widgets",
            os.path.join(GLib.get_user_config_dir(), "Kvantum"),
            "*.kvconfig", 1, checkKvantumFile
        )
        self.kvantumSearchableThemeList.setThemesTreeViewModel(getAvailableKvantumThemes())

    @Gtk.Template.Callback()
    def onSettingChanged(self, *args):
        """
        Whenever an option is changed, this function is called,
        either being defined as one of the callback functions from the 'window.ui' file,
        either as the callback function of SearchableThemeList's.

        Its goal is to enable the 'Apply' button(s),
        that get disabled whenever the settings are applied.
        """
        self.gtkThemesApplyButton.set_sensitive(True)
        self.iconThemesApplyButton.set_sensitive(True)
        self.cursorThemesApplyButton.set_sensitive(True)
        self.editCssApplyButton.set_sensitive(True)
        self.otherOptionsApplyButton.set_sensitive(True)
