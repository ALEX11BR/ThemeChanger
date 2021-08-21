# ThemeChanger
This app is a theme changing utility for Linux, BSDs, and whatnots.
It lets the user change GTK 2/3/4, icon and cursor themes, edit GTK CSS with live preview, and set some related options.
It also lets the user install icon and widget theme archives.

# Installation
## From source
Make sure you have installed PyGobject, Gtk3, GLib (for the app running), meson, ninja (for the installation process).

In the folder with the source (obtainable e.g. by running `git clone https://github.com/ALEX11BR/ThemeChanger`) run `meson build`, then `ninja -C build install`, and you're ready to go!

# TODOs
- Fix the bug in which after typing a text matching the currently selected widget theme in its selector, it gets unset
- In the themes list add an identifying image for ~~each theme~~ cursor themes (for GTK and icon themes they're implemented), as they require use of libXcursor, which doesn't have a Python binding yet (see some C implementations from [XFCE](https://gitlab.xfce.org/xfce/xfce4-settings/-/blob/master/dialogs/mouse-settings/main.c#L175) and [MATE](https://github.com/mate-desktop/mate-control-center/blob/master/capplets/common/mate-theme-info.c#L498))
- Add some sort of Kvantum support
- Add more options to set (see [further reference](https://developer.gnome.org/gtk3/stable/GtkSettings.html))
- Add theme remover
- Add a client for OCS-compatible websites like gnome-look.org, tailored for downloading (and automatically installing) themes (see [API reference]() and [a reference project](https://www.opencode.net/dfn2/pling-store-development))
- Use a cleaner CSS live preview method
- Clean the code overall
